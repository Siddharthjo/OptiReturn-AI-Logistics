import React, { useState, useEffect } from 'react';
import './Predict.css';

const Predict = () => {
  const [formData, setFormData] = useState({
    price: '',
    delivery_time: '',
    low_price: '',
    high_density_city: '',
    review_score: '',
    freight_value: '',
    customer_city: '',
    customer_state: '',
    order_status: ''
  });

  const [prediction, setPrediction] = useState(null);
  const [cities, setCities] = useState([]);
  const [states, setStates] = useState([]);
  const [orderStatuses, setOrderStatuses] = useState([]);

  // Fetch dataset and extract unique values for dropdowns
  useEffect(() => {
    const fetchDataset = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/get-dataset'); // Assume this endpoint fetches the dataset
        const data = await response.json();
        
        const uniqueCities = [...new Set(data.map(item => item.customer_city))];
        const uniqueStates = [...new Set(data.map(item => item.customer_state))];
        const uniqueOrderStatuses = [...new Set(data.map(item => item.order_status))];

        setCities(uniqueCities);
        setStates(uniqueStates);
        setOrderStatuses(uniqueOrderStatuses);
      } catch (err) {
        console.error('Error fetching dataset:', err);
      }
    };

    fetchDataset();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const isValid = Object.values(formData).every((value) => value !== '');
    if (!isValid) {
      alert('Please fill all fields');
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:8000/predict-return/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const data = await response.json();
        setPrediction(data.prediction);
      } else {
        setPrediction('Error: Unable to fetch prediction');
      }
    } catch (err) {
      console.error('Error:', err);
      setPrediction('Error: Unable to fetch prediction');
    }
  };

  return (
    <div className="predict-container">
      <h1>Product Return Prediction</h1>
      <form onSubmit={handleSubmit}>
        {/* Price Input */}
        <div className="input-group">
          <label>Price</label>
          <input
            type="number"
            name="price"
            value={formData.price}
            onChange={handleChange}
          />
        </div>

        {/* Delivery Time Input */}
        <div className="input-group">
          <label>Delivery Time (days)</label>
          <input
            type="number"
            name="delivery_time"
            value={formData.delivery_time}
            onChange={handleChange}
          />
        </div>

        {/* Low Price Input (Checkbox or Dropdown) */}
        <div className="input-group">
          <label>Low Price</label>
          <select
            name="low_price"
            value={formData.low_price}
            onChange={handleChange}
          >
            <option value="">Select</option>
            <option value="1">Low Price</option>
            <option value="0">Not Low Price</option>
          </select>
        </div>

        {/* High Density City Input (Dropdown) */}
        <div className="input-group">
          <label>High Density City</label>
          <select
            name="high_density_city"
            value={formData.high_density_city}
            onChange={handleChange}
          >
            <option value="">Select</option>
            <option value="1">Yes</option>
            <option value="0">No</option>
          </select>
        </div>

        {/* Review Score Input */}
        <div className="input-group">
          <label>Review Score</label>
          <input
            type="number"
            name="review_score"
            value={formData.review_score}
            onChange={handleChange}
          />
        </div>

        {/* Freight Value Input */}
        <div className="input-group">
          <label>Shipping Charge</label>
          <input
            type="number"
            name="freight_value"
            value={formData.freight_value}
            onChange={handleChange}
          />
        </div>

        {/* Customer State Input (Dropdown with values from the dataset) */}
        <div className="input-group">
          <label>State</label>
          <select
            name="customer_state"
            value={formData.customer_state}
            onChange={handleChange}
          >
            <option value="">Select State</option>
            {states.length > 0 ? (
              states.map((state) => (
                <option key={state} value={state}>
                  {state}
                </option>
              ))
            ) : (
              <option disabled>Loading states...</option>
            )}
          </select>
        </div>

                {/* Customer City Input (Dropdown with values from the dataset) */}
                <div className="input-group">
          <label>City</label>
          <select
            name="customer_city"
            value={formData.customer_city}
            onChange={handleChange}
          >
            <option value="">Select City</option>
            {cities.length > 0 ? (
              cities.map((city) => (
                <option key={city} value={city}>
                  {city}
                </option>
              ))
            ) : (
              <option disabled>Loading cities...</option>
            )}
          </select>
        </div>

        {/* Order Status Input (Dropdown with values from the dataset) */}
        <div className="input-group">
          <label>Order Status</label>
          <select
            name="order_status"
            value={formData.order_status}
            onChange={handleChange}
          >
            <option value="">Select Status</option>
            {orderStatuses.length > 0 ? (
              orderStatuses.map((status) => (
                <option key={status} value={status}>
                  {status}
                </option>
              ))
            ) : (
              <option disabled>Loading statuses...</option>
            )}
          </select>
        </div>

        <button type="submit">Get Prediction</button>
      </form>

      {prediction !== null && (
        <div className="prediction-result">
          <h2>Prediction: {prediction >= 0.4 ? "Likely to be Returned" : "Not Likely to be Returned"}</h2>
        </div>
      )}
    </div>
  );
};

export default Predict;