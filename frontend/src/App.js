import "./App.css";
import { Input } from "antd";
import { useNavigate } from "react-router-dom";

const { Search } = Input;

function App() {
  const navigate = useNavigate();
  const onSearch = (value, _e, info) => {
    console.log(info?.source, value);
    navigate(`/search?input=${value}`);
  };

  return (
    <div className="App">
      <div className="App-title">
        <div className="App-header">CSIT 5930 Search Engine</div>
        <div className="App-input">
          <Search
            placeholder="input search text"
            size="large"
            onSearch={onSearch}
            enterButton
          />
        </div>
        <div className="App-result"></div>
      </div>
    </div>
  );
}

export default App;
