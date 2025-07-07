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
              className={`message-container ${
                msg.sender === "user" ? "user-container" : "bot-container"
              }`}
              key={idx}
            >
              <div
                className={`message ${
                  msg.sender === "user" ? "user-message" : "bot-message"
                }`}
              >
                <strong>{msg.sender === "user" ? "You" : "Bot"}:</strong>{" "}
                {msg.text}
              </div>
              <button
                onClick={() => setReplyTo(msg.text)}
                className="reply-button"
                title="Reply"
              >
                <svg
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M10 9V5L3 12L10 19V14.9C15 14.9 18.5 16.5 21 20C20 15 17 10 10 9Z"
                    fill="#4a90e2"
                  />
                </svg>
              </button>
            </div>
          ))}
        </div>

        {replyTo && (
          <div className="replying-to">
            <div className="replying-indicator">
              <span>Replying to:</span>
              <div className="replying-content">{replyTo}</div>
            </div>
            <button
              onClick={() => setReplyTo(null)}
              className="cancel-reply-button"
              aria-label="Cancel reply"
            >
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z"
                  fill="#555"
                />
              </svg>
            </button>
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
