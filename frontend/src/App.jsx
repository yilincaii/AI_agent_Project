import { useState } from 'react'
import ChatPanel from './components/ChatPanel'
import AgentFlow from './components/AgentFlow'
import MessageBubble from './components/MessageBubble'

function App() {
  const [agentSteps, setAgentSteps] = useState([]);

  return (
    <div className="h-screen flex bg-gray-900 text-white">
      <div className="flex-1 flex flex-col border-r border-gray-700">
        <ChatPanel/>
      </div>

      <div className="w-1/3 p-4 overflow-y-auto">
        <AgentFlow/>
      </div>
    </div>
  );
}

export default App
