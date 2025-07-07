import React, { useState, FormEvent, ChangeEvent } from "react";
import { useNavigate } from "react-router-dom";
import "./authPages.css";

interface LoginResponse {
  idToken?: string;
  error?: {
    message?: string;
  };
}

const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [error, setError] = useState<string>("");

  const handleLogin = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");

    try {
      const response = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      const data: LoginResponse = await response.json();

      if (response.ok && data.idToken) {
        localStorage.setItem("userToken", data.idToken);
        navigate("/");
      } else {
        setError(data.error?.message || "Invalid email or password");
      }
    } catch (err) {
      setError("Something went wrong. Try again later.");
      console.error(err);
    }
  };

  const handleCreateAccount = () => {
    navigate("/signup");
  };

  return (
    <div className="login-page">
      <div className="auth-container">
        <div className="custom-auth-box">
          <h2>Login</h2>
          <form onSubmit={handleLogin}>
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e: ChangeEvent<HTMLInputElement>) =>
                setEmail(e.target.value)
              }
              required
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e: ChangeEvent<HTMLInputElement>) =>
                setPassword(e.target.value)
              }
              required
            />
            <button type="submit">Login</button>
            {error && <p className="error">{error}</p>}
          </form>

          <div className="create-account-container">
            <p>Don't have an account?</p>
            <button
              onClick={handleCreateAccount}
              className="create-account-button"
            >
              Create Account
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
