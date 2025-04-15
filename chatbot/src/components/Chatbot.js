import { useState, useEffect, useRef } from "react";
import "./Chatbot.css"; // Import the CSS file

export default function LoanChatbot() {
  const [messages, setMessages] = useState([
    { text: "Welcome! Let's check your loan eligibility. Please enter your number of dependents.", sender: "bot" }
  ]);
  const [userInput, setUserInput] = useState("");
  const [currentStep, setCurrentStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const chatEndRef = useRef(null); // Reference for auto-scrolling

  const prompts = [
    "Enter your annual income:",
    "Enter the loan amount you need:",
    "Enter the loan term (in months):",
    "Enter your CIBIL score (300-900):",
    "Enter your residential assets value:",
    "Enter your commercial assets value:",
  ];

  const [userResponses, setUserResponses] = useState([]);

  // Auto-scroll to the latest message
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!userInput.trim()) return;

    const newMessages = [...messages, { text: userInput, sender: "user" }];
    const newResponses = [...userResponses, userInput];
    setUserResponses(newResponses);
    setUserInput("");
    setMessages(newMessages);
    setError(null);
    
    setLoading(true);

    setTimeout(async () => {
      setLoading(false);
      if (currentStep < prompts.length) {
        setMessages([...newMessages, { text: prompts[currentStep], sender: "bot" }]);
        setCurrentStep(currentStep + 1);
      } else {
        try {
          // Convert all inputs to their appropriate types
          const payload = {
            no_of_dependents: parseInt(newResponses[0]),
            income_annum: parseFloat(newResponses[1]),
            loan_amount: parseFloat(newResponses[2]),
            loan_term: parseInt(newResponses[3]),
            cibil_score: parseInt(newResponses[4]),
            residential_assets_value: parseFloat(newResponses[5]),
            commercial_assets_value: parseFloat(userInput),
          };
          
          // Validate inputs to prevent API errors
          for (const [key, value] of Object.entries(payload)) {
            if (isNaN(value)) {
              throw new Error(`Invalid input for ${key}. Please enter a number.`);
            }
          }

          const response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
          });
          
          
          if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Failed to get prediction");
          }

          const data = await response.json();
          console.log("📩 Response from backend:", data);
          
          const resultMessage =
            data.loan_status === "Approved"
              ? "🎉 Congratulations! You are eligible for the loan."
              : "❌ Sorry, based on your information, you are not eligible for the loan.";

          setMessages([...newMessages, { text: resultMessage, sender: "bot" }]);
          
          // Add option to restart
          setTimeout(() => {
            setMessages(prev => [...prev, { 
              text: "Would you like to check eligibility for another loan? Type 'restart' to begin again.", 
              sender: "bot" 
            }]);
          }, 1000);
        } catch (err) {
          console.error("Error:", err);
          setError(err.message);
          setMessages([...newMessages, { 
            text: `Error: ${err.message}. Please try again.`, 
            sender: "bot" 
          }]);
        }
      }
    }, 1000);
  };

  // Handle "Enter" key to send message
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleSend();
    }
  };

  // Reset chatbot if user types "restart"
  useEffect(() => {
    const lastUserMessage = messages.filter(m => m.sender === "user").pop();
    if (lastUserMessage && lastUserMessage.text.toLowerCase() === "restart") {
      setMessages([
        { text: "Welcome! Let's check your loan eligibility. Please enter your number of dependents.", sender: "bot" }
      ]);
      setUserResponses([]);
      setCurrentStep(0);
      setError(null);
    }
  }, [messages]);

  return (
    <div className="chat-container">
      {/* Header Section */}
      <div className="header">Loan Eligibility Prediction</div>
  
      {/* Chat Box */}
      <div className="chat-box">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message ${
              msg.sender === "bot" ? "bot-message" : "user-message"
            }`}
          >
            {msg.text}
          </div>
        ))}
        {loading && <div className="typing">Typing...</div>}
        {error && <div className="error-message">Error: {error}</div>}
        <div ref={chatEndRef} />
      </div>
  
      {/* Input Box */}
      <div className="input-box">
        <input
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your response..."
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
  
}