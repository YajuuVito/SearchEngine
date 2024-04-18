import "./Search.css";
import { Input, Radio, Spin } from "antd";
import { useCallback, useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";

const { Search } = Input;

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
                <a href={"https://" + item.url} target="_blank" key={item.id}>
                  {item.title}
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
                <a href={"https://" + item.url} target="_blank" key={item.id}>
                  {item.title}
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
  const [mode, setMode] = useState("page_rank");
  const [loading, setLoading] = useState(false);

  const onChange = (e) => {
    console.log("radio checked", e.target.value);
    setMode(e.target.value);
  };

  const searchAction = async (value, mode) => {
    setLoading(true);
    const res = await axios.get(
      `http://localhost:8000/SE/search?words=${value}&mode=${mode}`
    );
    console.log(res);
    const docList = res.data.doc_rank.map((item) => {
      const frequency_list = {}
      item.freq.forEach(pair=>{
        frequency_list[pair[0]] = pair[1]
      })
      return {
        title: item.Title,
        url: item.URL,
        date: item["Last Modified"],
        size: item.Size,
        parent_link: item["parent_id"],
        child_link: item["child_id"],
        frequency_list
      };
    });
    setResult(docList);
    setLoading(false);
  };
  const onSearch = (value, _e, info) => {
    navigate(`/search?input=${value}`);
    const textList = value.split(" ").filter((item) => item != "");
    console.log(textList);
    searchAction(value, mode);
  };
  const getInput = useCallback(() => {
    const searchValue = location.search.split("=")[1];
    return searchValue;
  }, [location]);

  useEffect(() => {
    const value = getInput();
    const decodeValue = decodeURIComponent(value);
    setInputValue(decodeValue);
    searchAction(value, "page_rank");
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
          <Radio.Group onChange={onChange} value={mode}>
            <Radio value={"vsm"}>Vector Space Model</Radio>
            <Radio value={"page_rank"}>Page Rank</Radio>
          </Radio.Group>
        </div>
        <Spin spinning={loading}>
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
        </Spin>
      </div>
    </div>
  );
}

export default SearchPage;
