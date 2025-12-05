"use client";

import { useState, FormEvent } from "react";

type Citation = {
  file_name: string;
  page: number;
};

type Message = {
  role: "user" | "ai";
  text: string;
  citations?: Citation[];
};

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [doorSchedule, setDoorSchedule] = useState<any[]>([]);


  // Backend base URL – your FastAPI
  const API_BASE = "http://127.0.0.1:8000";

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError("");

    const trimmed = input.trim();
    if (!trimmed) return;

    const userMessage: Message = { role: "user", text: trimmed };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: trimmed }),
      });

      if (!res.ok) {
        throw new Error(`Backend error: ${res.status}`);
      }

      const data = await res.json();

      const aiMessage: Message = {
        role: "ai",
        text: data.answer ?? "No answer received from backend",
        citations: data.citations ?? [],
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (err) {
      console.error(err);
      setError(
        "Could not reach backend. Is FastAPI running on http://127.0.0.1:8000?"
      );
    } finally {
      setLoading(false);
    }
  }
  async function fetchDoorSchedule() {
  setError("");

  try {
    const res = await fetch(`${API_BASE}/door-schedule`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({}),
    });

    if (!res.ok) {
      throw new Error(`Backend error: ${res.status}`);
    }

    const data = await res.json();
    setDoorSchedule(data.rows ?? []);
  } catch (err) {
    console.error(err);
    setError("Failed to fetch door schedule. Is backend running?");
  }
}


  return (
    <main
      style={{
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        padding: "16px",
        maxWidth: "800px",
        margin: "0 auto",
      }}
    >
      <h1 style={{ fontSize: "24px", fontWeight: "bold", marginBottom: "12px" }}>
        Project Brain – Chat (Keyword Mode)
      </h1>

      <div
        style={{
          flex: 1,
          border: "1px solid #444",
          borderRadius: "8px",
          padding: "12px",
          overflowY: "auto",
          marginBottom: "12px",
        }}
      >
        {messages.length === 0 && (
          <div style={{ color: "#777" }}>No messages yet. Try asking something that exists in the PDF.</div>
        )}

        {messages.map((m, idx) => (
          <div
            key={idx}
            style={{
              marginBottom: "10px",
              textAlign: m.role === "user" ? "right" : "left",
            }}
          >
            <div
              style={{
                display: "inline-block",
                padding: "8px 10px",
                borderRadius: "8px",
                background:
                  m.role === "user" ? "#2563eb" : "rgba(107,114,128,0.25)",
                color: m.role === "user" ? "white" : "inherit",
                maxWidth: "80%",
                whiteSpace: "pre-wrap",
              }}
            >
              {m.text}
            </div>

            {m.role === "ai" && m.citations && m.citations.length > 0 && (
              <div
                style={{
                  fontSize: "12px",
                  marginTop: "3px",
                  opacity: 0.7,
                }}
              >
                Sources:&nbsp;
                {m.citations
                  .map((c) => `${c.file_name} (p. ${c.page})`)
                  .join(", ")}
              </div>
            )}
          </div>
        ))}
      </div>

      {error && (
        <div style={{ color: "red", marginBottom: "8px" }}>{error}</div>
      )}

      <form
        onSubmit={handleSubmit}
        style={{ display: "flex", gap: "8px", marginTop: "auto" }}
      >
        <button
  onClick={fetchDoorSchedule}
  style={{
    marginTop: "10px",
    border: "1px solid #666",
    padding: "8px 12px",
    borderRadius: "6px",
    background: "transparent",
    cursor: "pointer",
  }}
>
  Generate Door Schedule
</button>

        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask something about the documents..."
          style={{
            flex: 1,
            padding: "8px",
            borderRadius: "6px",
            border: "1px solid #666",
            background: "transparent",
            color: "inherit",
          }}
        />
        <button
          type="submit"
          disabled={loading}
          style={{
            padding: "8px 12px",
            borderRadius: "6px",
            border: "none",
            cursor: "pointer",
            opacity: loading ? 0.7 : 1,
          }}
        >
          {loading ? "Sending..." : "Send"}
        </button>
        {doorSchedule.length > 0 && (
  <div style={{ marginTop: "16px" }}>
    <h3 style={{ fontSize: "18px", fontWeight: "bold" }}>
      Extracted Door Schedule
    </h3>

    <table
      style={{
        width: "100%",
        borderCollapse: "collapse",
        marginTop: "8px",
      }}
    >
      <thead>
        <tr style={{ background: "rgba(255,255,255,0.1)" }}>
          <th style={{ border: "1px solid #444", padding: "6px" }}>File</th>
          <th style={{ border: "1px solid #444", padding: "6px" }}>Page</th>
          <th style={{ border: "1px solid #444", padding: "6px" }}>
            Extracted Line
          </th>
        </tr>
      </thead>
      <tbody>
        {doorSchedule.map((row, idx) => (
          <tr key={idx}>
            <td style={{ border: "1px solid #444", padding: "6px" }}>
              {row.file_name}
            </td>
            <td style={{ border: "1px solid #444", padding: "6px" }}>
              {row.page}
            </td>
            <td style={{ border: "1px solid #444", padding: "6px" }}>
              {row.line}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
)}

      </form>
    </main>
  );
}
