import React, { useState, useEffect } from 'react';

const ResalePredict = () => {
  const [formData, setFormData] = useState({
    price: '',
    review_score: '',
    freight_value: '',
    customer_city: '',
    customer_state: '',
    order_status: ''
  });

  const [prediction, setPrediction] = useState(null);
  const [cities, setCities] = useState([]);
  const [states, setStates] = useState([]);
  const [statuses, setStatuses] = useState([]);
  // const [loading, setLoading] = useState(true);

  // Fetch dataset and extract unique values
  useEffect(() => {
    const fetchDataset = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/get-dataset');
        const data = await response.json();
        console.log("Fetched dataset:", data);

        const uniqueCities = [...new Set(data.map(item => item.customer_city).filter(Boolean))];
        const uniqueStates = [...new Set(data.map(item => item.customer_state).filter(Boolean))];
        const uniqueOrderStatuses = [...new Set(data.map(item => item.order_status).filter(Boolean))];

        setCities(uniqueCities);
        setStates(uniqueStates);
        setStatuses(uniqueOrderStatuses);
      } catch (err) {
        console.error('Error fetching dataset:', err);
      } 
      // finally {
      //   setLoading(false);
      // }
    };

    fetchDataset();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Form submission triggered");

    // Simple validation for required fields
    // Diff
    if (
      !formData.price ||
      !formData.review_score ||
      !formData.freight_value ||
      !formData.customer_city ||
      !formData.customer_state ||
      !formData.order_status
    ) {
      alert('Please fill all fields');
      return;
    }

    // Validate if the numerical fields are valid
    // Diff
    if (isNaN(formData.price) || isNaN(formData.freight_value) || isNaN(formData.review_score)) {
      alert('Price, Freight Value, and Review Score must be valid numbers');
      return;
    }

    console.log("Form Data:", formData);

    try {
      const response = await fetch('http://127.0.0.1:8000/predict-resale/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        const data = await response.json();
        console.log("Prediction result:", data);
        setPrediction(data.predicted_resale_value);
      } else {
        console.error("Failed to fetch prediction:", response.statusText);
        setPrediction('Error: Unable to fetch prediction');
      }
    } catch (err) {
      console.error("Error during API request:", err);
      setPrediction('Error: Unable to fetch prediction');
    }
  };

  // if (loading) {
  //   return <div>Loading dataset...</div>;
  // }

  return (
    <div className="predict-container">
      <h1>Resale Value Prediction</h1>
      <form onSubmit={handleSubmit}>
        {/* Product Price */}
        <div className="input-group">
          <label>Product Price</label>
          <input
            type="number"
            name="price"
            value={formData.price}
            onChange={handleChange}
            step="0.01"
          />
        </div>

        {/* Review Score */}
        <div className="input-group">
          <label>Review Score</label>
          <input
            type="number"
            name="review_score"
            value={formData.review_score}
            onChange={handleChange}
            step="0.1"
            min="0"
            max="5"
          />
        </div>

        {/* Shipping Charge */}
        <div className="input-group">
          <label>Shipping Charge</label>
          <input
            type="number"
            name="freight_value"
            value={formData.freight_value}
            onChange={handleChange}
            step="0.01"
          />
        </div>

        {/* Customer City */}
        <div className="input-group">
          <label>Customer City</label>
          <select
            name="customer_city"
            value={formData.customer_city}
            onChange={handleChange}
          >
            <option value="">Select</option>
            {/* Change */}
            {cities.map((city) => (
              <option key={city} value={city}>
                {city}
              </option>
            ))}
          </select>
        </div>

        {/* Customer State */}
        <div className="input-group">
          <label>Customer State</label>
          <select
            name="customer_state"
            value={formData.customer_state}
            onChange={handleChange}
          >
            <option value="">Select</option>
            {states.map((state) => (
              <option key={state} value={state}>{state}</option>
            ))}
          </select>
        </div>

        {/* Order Status */}
        <div className="input-group">
          <label>Order Status</label>
          <select
            name="order_status"
            value={formData.order_status}
            onChange={handleChange}
          >
            <option value="">Select</option>
            {statuses.map((status) => (
              <option key={status} value={status}>{status}</option>
            ))}
          </select>
        </div>

        <button type="submit">Predict Resale Value</button>
      </form>

      {prediction !== null && (
        <div className="prediction-result">
          <h2>Predicted Resale Value: {Number(prediction).toFixed(2)}</h2>
        </div>
      )}
      {console.log(prediction)}
    </div>
  );
};

export default ResalePredict;