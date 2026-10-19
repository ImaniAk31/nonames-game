import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HostScreen from './components/HostScreen';
import ClientScreen from './components/ClientScreen';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ClientScreen />} />
        <Route path="/host" element={<HostScreen />} />
      </Routes>
    </Router>
  );
}

export default App;