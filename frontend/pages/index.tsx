import { useState } from 'react'
import useSWRMutation from 'swr/mutation'

async function sendChat(url: string, { arg }: { arg: { question: string } }) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(arg),
  })
  return res.json()
}

export default function Home() {
  const [question, setQuestion] = useState('')
  const { trigger, data, isMutating } = useSWRMutation(
    process.env.NEXT_PUBLIC_API_URL + '/chat',
    sendChat
  )

  const ask = async () => {
    if (!question.trim()) return
    await trigger({ question })
    setQuestion('')
  }

  return (
    <div className="min-h-screen flex flex-col items-center bg-gray-100 py-10">
      <h1 className="text-3xl font-semibold mb-6">🎓 Kellogg Chat Assistant</h1>
      <div className="w-full max-w-2xl space-y-4">
        {data && (
          <div className="p-4 bg-white rounded shadow">
            <p className="whitespace-pre-wrap">{data.answer || JSON.stringify(data)}</p>
          </div>
        )}
        <div className="flex">
          <input
            className="flex-grow px-4 py-2 border rounded-l"
            placeholder="Ask a question…"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && ask()}
          />
          <button
            onClick={ask}
            className="px-4 py-2 bg-purple-600 text-white rounded-r disabled:opacity-50"
            disabled={isMutating}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  )
}
