import "./Search.css";
import { Input } from "antd";
import { useCallback, useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

const { Search } = Input;

const mockRes = {
  data: [
    {
      title: "computer page 1",
      url: "www.baidu.com",
      date: "Sat, 13 Apr 2024 14:45:26 GMT",
      size: 2,
      parent_link: ["1.com", "2.com"],
      child_link: ["1.com", "2.com"],
      frequency_list: {
        computer: 5,
        science: 4,
        network: 4,
        AI: 3,
        search: 2,
      },
    },
    {
      title: "computer page 2",
      url: "www.baidu.com",
      date: "Sat, 13 Apr 2024 14:45:26 GMT",
      size: 2,
      parent_link: ["1.com", "2.com"],
      child_link: ["1.com", "2.com"],
      frequency_list: {
        computer: 5,
        science: 4,
        network: 4,
        AI: 3,
        search: 2,
      },
    },
  ],
};

function Result(props) {
  const { title, url, date, size, parent_link, child_link, frequency_list } =
    props;
  return (
    <div style={{ marginBottom: "20px" }}>
      <a href={"https://" + url} target="_blank">
        {url}
      </a>
      <div style={{ fontSize: "25px", fontWeight: "bold" }}>{title}</div>
      <div style={{ fontSize: "10px", color: "gray" }}>
        last modified date: <span style={{ color: "black" }}>{date}</span>; page
        size: <span style={{ color: "black" }}>{size}</span>
      </div>
      <div style={{ display: "flex", width: "500px", color: "#4d5156" }}>
        <div style={{ width: "150px" }}>
          <div>Top-5 Keywords</div>
          {Object.keys(frequency_list).map((item) => {
            return (
              <div key={item}>
                {item} : {frequency_list[item]}
              </div>
            );
          })}
        </div>
        <div style={{ width: "150px" }}>
          <div>Parent Links</div>
          <div>
            {parent_link.map((item) => (
              <div>
                <a href={"https://" + item} target="_blank" key={item}>
                  {item}
                </a>
              </div>
            ))}
          </div>
        </div>
        <div style={{ width: "150px" }}>
          <div>Child Links</div>
          <div>
            {child_link.map((item) => (
              <div>
                <a href={"https://" + item} target="_blank" key={item}>
                  {item}
                </a>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function SearchPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const [inputValue, setInputValue] = useState("");
  const [result, setResult] = useState([]);

  const searchAction = () => {
    setResult(mockRes["data"]);
  };
  const onSearch = (value, _e, info) => {
    navigate(`/search?input=${value}`);
    const textList = value.split(" ").filter((item) => item != "");
    console.log(textList);
    searchAction();
  };
  const getInput = useCallback(() => {
    const searchValue = location.search.split("=")[1];
    return searchValue;
  }, [location]);

  useEffect(() => {
    const value = getInput();
    const decodeValue = decodeURIComponent(value);
    setInputValue(decodeValue);
    searchAction();
  }, []);
  return (
    <div className="Search">
      <div className="Search-title">
        <div className="Search-header">CSIT 5930 Search Engine</div>
        <div className="Search-input">
          <Search
            placeholder="input search text"
            size="large"
            onSearch={onSearch}
            value={inputValue}
            onChange={({ value }) => setInputValue(value)}
            enterButton
          />
        </div>
        <div className="Search-result">
          {result.map((item) => {
            const {
              title,
              url,
              date,
              size,
              parent_link,
              child_link,
              frequency_list,
            } = item;
            return (
              <Result
                key={title}
                title={title}
                url={url}
                date={date}
                size={size}
                parent_link={parent_link}
                child_link={child_link}
                frequency_list={frequency_list}
              />
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default SearchPage;
