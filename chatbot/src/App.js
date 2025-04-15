import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import LoanChatbot from "./components/Chatbot";

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<LoanChatbot />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
