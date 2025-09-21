import { motion } from "framer-motion";

export default function MessageBubble({ message }) {
  const isUser = message.role === "user";

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 10 }}
      transition={{ duration: 0.3 }}
      className={`flex ${isUser ? "justify-end" : "justify-start"}`}
    >
      <div
        className={`
          max-w-xs px-4 py-2 rounded-lg shadow-md break-words
          ${isUser 
            ? "bg-blue-600 text-white rounded-br-none" 
            : "bg-gray-700 text-white rounded-bl-none"}
        `}
      >
        {message.content}
      </div>
    </motion.div>
  );
}