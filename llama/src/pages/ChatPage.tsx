import React, { useState, ChangeEvent, FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import "./chatPage.css";

interface ChatMessage {
  sender: "user" | "bot";
  text: string;
}

const ChatPage: React.FC = () => {
  const navigate = useNavigate();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [replyTo, setReplyTo] = useState<string | null>(null);

  const [input, setInput] = useState<string>("");
  const [error, setError] = useState<string>("");

  const handleSend = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    const trimmed = input.trim();
    if (!trimmed) return;

    const userMsg: ChatMessage = { sender: "user", text: trimmed };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");

    try {
      const payload: any = { message: trimmed };
      if (replyTo) payload.reply_to = replyTo;

      const response = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok || !data.response) {
        setError(data.error || "Error getting response");
        return;
      }

      const botMsg: ChatMessage = { sender: "bot", text: data.response };
      setMessages((prev) => [...prev, botMsg]);
      setReplyTo(null);
    } catch (err) {
      console.error(err);
      setError("Failed to connect to server.");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("userToken");
    navigate("/login");
  };

  return (
    <div className="chat-page">
      <div className="chat-container">
        <button onClick={handleLogout} className="logout-button">
          Logout
        </button>
        <h2>Chat</h2>

        <div className="messages-container">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`message ${
                msg.sender === "user" ? "user-message" : "bot-message"
              }`}
            >
              <strong>{msg.sender === "user" ? "You" : "Bot"}:</strong>{" "}
              {msg.text}
              <button
                onClick={() => setReplyTo(msg.text)}
                className="reply-button"
              >
                Reply
              </button>
            </div>
          ))}
        </div>

        {replyTo && (
          <div className="replying-to">
            Replying to: <em>{replyTo}</em>
            <button onClick={() => setReplyTo(null)}>Cancel</button>
          </div>
        )}
        <form onSubmit={handleSend} className="input-form">
          <input
            type="text"
            placeholder="Type your message..."
            value={input}
            onChange={(e: ChangeEvent<HTMLInputElement>) =>
              setInput(e.target.value)
            }
          />
          <button type="submit">Send</button>
        </form>

        {error && <p className="error">{error}</p>}
      </div>
    </div>
  );
};

export default ChatPage;
