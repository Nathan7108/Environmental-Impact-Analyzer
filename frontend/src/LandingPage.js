import React, { useState } from 'react';
import './LandingPage.css';

const LandingPage = () => {
  const [searchInput, setSearchInput] = useState(''); // State for search bar input
  const [results, setResults] = useState([]); // State for storing search results

  // Handle search bar input change
  const handleInputChange = (e) => {
    setSearchInput(e.target.value);
  };

  // Fetch analysis from backend
  const analyzeProduct = async (productName) => {
    try {
      const response = await fetch('http://127.0.0.1:8080/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ product_name: productName }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch analysis from the backend');
      }

      const data = await response.json();
      return data.analysis;
    } catch (error) {
      console.error('Error fetching analysis:', error);
      return 'Unable to analyze the product.';
    }
  };

  // Handle the search button click
  const handleSearch = async () => {
    if (searchInput.trim() === '') {
      alert('Please enter a search term.');
      return;
    }

    const analysis = await analyzeProduct(searchInput);
    setResults([{ name: searchInput, analysis }]);
  };

  return (
    <div className="landing-page">
      <div className="content">
        <h1>Welcome to the Environmental Impact Analyzer</h1>
        <p>Discover the hidden impact of everyday products and make eco-friendly choices.</p>
        <input
          type="text"
          placeholder="Search for a product..."
          className="search-bar"
          value={searchInput}
          onChange={handleInputChange}
        />
        <button className="cta-button" onClick={handleSearch}>
          Explore Now
        </button>
        {/* Display search results */}
        <div className="search-results">
          {results.length > 0 ? (
            <ul>
              {results.map((item, index) => (
                <li key={index}>
                  <strong>{item.name}</strong>: {item.analysis}
                </li>
              ))}
            </ul>
          ) : (
            searchInput && <p>No results found.</p>
          )}
        </div>
      </div>
      <div className="background-animation"></div>
    </div>
  );
};

export default LandingPage;
