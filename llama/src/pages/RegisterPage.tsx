import React, { useState, FormEvent, ChangeEvent } from "react";
import { useNavigate } from "react-router-dom";
import "./authPages.css";

interface RegisterResponse {
  idToken?: string;
  error?: {
    message?: string;
  };
}

const RegisterPage: React.FC = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [confirmPassword, setConfirmPassword] = useState<string>("");
  const [error, setError] = useState<string>("");

  const handleRegister = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      const data: RegisterResponse = await response.json();
      console.log("Response status:", response.status);
      console.log("Response data:", data);

      if (response.ok && data.idToken) {
        localStorage.setItem("userToken", data.idToken);
        navigate("/");
      } else {
        setError(data.error?.message || "Registration failed");
      }
    } catch (err) {
      setError("Something went wrong. Try again later.");
      console.error(err);
    }
  };

  return (
    <div className="login-page">
      <div className="auth-container">
        <div className="custom-auth-box">
          <h2>Create Account</h2>
          <form onSubmit={handleRegister}>
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
            <input
              type="password"
              placeholder="Confirm Password"
              value={confirmPassword}
              onChange={(e: ChangeEvent<HTMLInputElement>) =>
                setConfirmPassword(e.target.value)
              }
              required
            />
            <button type="submit">Register</button>
            {error && <p className="error">{error}</p>}
          </form>
          <div className="create-account-container">
            <p>Already have an account?</p>
            <button
              className="create-account-button"
              onClick={() => navigate("/login")}
            >
              Login
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;
