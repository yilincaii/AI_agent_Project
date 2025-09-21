import { useState } from "react";
import MessageBubble from "./MessageBubble";

export default function ChatPanel({ setAgentSteps }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    setMessages((prev) => [...prev, { role: "user", content: input }]);
    const userInput = input;
    setInput("");

    try {
      const res = await fetch("http://localhost:5050/prompt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: userInput }),
      });

    // 新增：非 2xx 直接抛错
    if (!res.ok || !res.body) {
    const text = await res.text().catch(() => "");
    throw new Error(`HTTP ${res.status} ${res.statusText} ${text}`);
    }
      const reader = res.body.getReader();
      const decoder = new TextDecoder("utf-8");

      let aiReply = "";
      let steps = [];

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split("\n\n").filter(Boolean);

        for (const line of lines) {
          if (line.startsWith("data:")) {
            const jsonStr = line.replace("data: ", "");
            try {
              const parsed = JSON.parse(jsonStr);
              console.log("SSE chunk:", parsed);

              // Supervisor reply
              if (parsed?.response?.supervisor?.content) {
                aiReply = parsed.response.supervisor.content;
              }

              // Dynamic agent flow capture
              const agentLike = Object.entries(parsed.response || {})
                .filter(([key]) => key !== "supervisor")
                .map(([role, obj]) => ({
                  type: role,
                  content: obj?.content || JSON.stringify(obj),
                }));

              if (agentLike.length) {
                steps = agentLike;
                setAgentSteps(steps);
              }
            } catch (err) {
              console.error("Bad SSE chunk", err);
            }
          }
        }
      }

      if (aiReply) {
        setMessages((prev) => [...prev, { role: "ai", content: aiReply }]);
      }
    } catch (err) {
      console.error("Chat error:", err);
    }
  };

  return (
    <div className="flex flex-col h-full border rounded-lg overflow-hidden">
      {/* Header */}
      <div className="bg-gray-900 text-white p-3 font-bold text-lg text-center">
        JARVIS ASSISTANT
      </div>

      {/* Scrollable messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {messages.map((msg, idx) => (
          <MessageBubble key={idx} message={msg} />
        ))}
      </div>

      {/* Input at bottom */}
      <div className="flex p-2 border-t border-gray-700">
        <input
          className="flex-1 p-2 rounded bg-gray-800 text-white outline-none"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Type a message..."
        />
        <button
          className="ml-2 px-4 py-2 bg-blue-600 rounded hover:bg-blue-700"
          onClick={sendMessage}
        >
          Send
        </button>
      </div>
    </div>
  );
}