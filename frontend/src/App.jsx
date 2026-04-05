import { useState } from 'react'
import './App.css'

function App() {
  const [borrowerId, setBorrowerId] = useState('B_0001')
  const [gciData, setGciData] = useState(null)
  const [anomalyData, setAnomalyData] = useState(null)
  const [error, setError] = useState('')

  const fetchDashboardData = async () => {
    setError('')
    try {
      // Ask the Waiter for the GCI Score
      const gciRes = await fetch(`http://localhost:8000/gci/${borrowerId}`)
      if (!gciRes.ok) throw new Error('Borrower not found in database')
      const gci = await gciRes.json()
      setGciData(gci)

      // Ask the Waiter for the Fraud/Anomaly flags
      const anomalyRes = await fetch(`http://localhost:8000/anomaly/${borrowerId}`)
      const anomaly = await anomalyRes.json()
      setAnomalyData(anomaly)
    } catch (err) {
      setError(err.message)
      setGciData(null)
      setAnomalyData(null)
    }
  }

  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial, sans-serif', maxWidth: '600px', margin: '0 auto' }}>
      <h1>Gig Cashflow Index</h1>
      <p>Evaluate creditworthiness using actual behavioral finance features.</p>
      
      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
        <input 
          type="text" 
          value={borrowerId} 
          onChange={(e) => setBorrowerId(e.target.value)}
          placeholder="Enter ID (e.g., B_0001)"
          style={{ padding: '10px', fontSize: '16px', flex: 1 }}
        />
        <button onClick={fetchDashboardData} style={{ padding: '10px 20px', fontSize: '16px', cursor: 'pointer' }}>
          Fetch Score
        </button>
      </div>

      {error && <p style={{ color: 'red', fontWeight: 'bold' }}>{error}</p>}

      {gciData && anomalyData && (
        <div style={{ padding: '20px', border: '2px solid #ccc', borderRadius: '10px', textAlign: 'left', backgroundColor: '#f9f9f9', color: '#333' }}>
          <h2>Borrower Profile: {gciData.borrower_id}</h2>
          
          <h3 style={{ fontSize: '2rem', margin: '10px 0', color: gciData.gci_score >= 600 ? 'green' : '#d97706' }}>
            GCI Score: {gciData.gci_score}
          </h3>
          
          <div style={{ marginTop: '20px', padding: '15px', backgroundColor: anomalyData.manipulation_label === 'clean' ? '#e6fffa' : '#ffe4e6', borderRadius: '8px' }}>
            <h4 style={{ margin: '0 0 10px 0' }}>Risk & Anomaly Detection</h4>
            <p style={{ margin: '5px 0' }}><strong>Status:</strong> {anomalyData.manipulation_label.toUpperCase()}</p>
            <p style={{ margin: '5px 0' }}><strong>Anomaly Score:</strong> {anomalyData.anomaly_score.toFixed(4)}</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default App