import "./Search.css";
import { Input, Radio, Spin, Button } from "antd";
import { useCallback, useEffect, useMemo, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";

const { Search } = Input;

function Result(props) {
  const {
    title,
    url,
    date,
    size,
    parent_link,
    child_link,
    frequency_list,
    searchAction,
    mode,
    score,
  } = props;
  return (
    <div
      style={{
        paddingBottom: "10px",
        marginBottom: "10px",
        borderBottom: "1px solid #1677ff",
      }}
    >
      <a href={url} target="_blank">
        {url}
      </a>
      <div style={{ fontSize: "25px", fontWeight: "bold" }}>{title}</div>
      <div style={{ fontSize: "15px", color: "gray" }}>
        last modified date: <span style={{ color: "black" }}>{date}</span>; page
        size: <span style={{ color: "black" }}>{size}</span>; score:{" "}
        <span style={{ color: "black" }}>{score.toFixed(5)}</span>
      </div>
      <div style={{ display: "flex", color: "#4d5156" }}>
        <div style={{ width: "150px" }}>
          <div>Top-5 Keywords</div>
          {Object.keys(frequency_list).map((item) => {
            return (
              <div key={item}>
                {item} : {frequency_list[item]}
              </div>
            );
          })}
          <a
            onClick={() =>
              searchAction(Object.keys(frequency_list).join(" "), mode)
            }
          >
            get similar pages
          </a>
        </div>
        <div style={{ width: "200px" }}>
          <div>Parent Links</div>
          <div>
            {parent_link.map((item) => (
              <div>
                <a href={item.url} target="_blank" key={item.id}>
                  {item.title}
                </a>
              </div>
            ))}
          </div>
        </div>
        <div style={{ width: "350px" }}>
          <div>Child Links</div>
          <div style={{ maxHeight: 150, overflowY: "scroll" }}>
            {child_link.map((item) => (
              <div>
                <a href={item.url} target="_blank" key={item.id}>
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

const KeywordList = (props) => {
  const { keywords } = props;
  const [num, setNum] = useState(50);
  const [list, setList] = useState(keywords.slice(0, 50));
  const addMore = () => {
    const currNum = num;
    setNum(currNum + 50);
    setList(keywords.slice(0, currNum + 50));
  };

  return (
    <div className="Keywords">
      <div style={{ fontSize: "25px", fontWeight: "bold" }}>Keywords List</div>
      {list.map((item) => {
        return <div key={item}>{item}</div>;
      })}
      <Button type="text" onClick={addMore}>
        load more keywords
      </Button>
    </div>
  );
};

function SearchPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const [inputValue, setInputValue] = useState("");
  const [result, setResult] = useState([]);
  const [mode, setMode] = useState("page_rank");
  const [loading, setLoading] = useState(false);
  const [keywords, setKeywords] = useState([]);

  const onChange = (e) => {
    setMode(e.target.value);
  };

  const searchAction = async (value, mode) => {
    setLoading(true);
    const decodeValue = decodeURIComponent(value);
    if (inputValue != decodeValue) {
      setInputValue(decodeValue);
    }
    const res = await axios.get(
      `http://localhost:8000/SE/search?words=${value}&mode=${mode}`
    );
    console.log(res);
    const docList = res.data.doc_rank.map((item) => {
      const frequency_list = {};
      item.freq.forEach((pair) => {
        frequency_list[pair[0]] = pair[1];
      });
      return {
        title: item.Title,
        url: item.URL,
        date: item["Last Modified"],
        size: item.Size,
        parent_link: item["parent_id"],
        child_link: item["child_id"],
        frequency_list,
        score: item["score"],
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

  const getKeywords = async () => {
    const res = await axios.get(`http://localhost:8000/SE/get_all_keywords`);
    console.log(res);
    setKeywords(res.data.keywords);
  };

  useEffect(() => {
    const value = getInput();
    const decodeValue = decodeURIComponent(value);
    setInputValue(decodeValue);
    searchAction(value, "page_rank");
    getKeywords();
  }, []);

  const onInputChange = (v) => {
    setInputValue(v.target.value);
  };

  return (
    <div className="Search">
      <div className="Search-title">
        <div className="top-box">
          <div className="Search-header">CSIT 5930 Search Engine</div>
          <div className="Search-input">
            <Search
              placeholder="input search text"
              size="large"
              onSearch={onSearch}
              value={inputValue}
              onChange={onInputChange}
              enterButton
            />
            <Radio.Group onChange={onChange} value={mode}>
              <Radio value={"vsm"}>Vector Space Model</Radio>
              <Radio value={"page_rank"}>Page Rank</Radio>
            </Radio.Group>
          </div>
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
                score,
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
                  searchAction={searchAction}
                  mode={mode}
                  score={score}
                />
              );
            })}
          </div>
          <Spin spinning={keywords.length === 0}>
            {keywords.length !== 0 && <KeywordList keywords={keywords} />}
          </Spin>
        </Spin>
      </div>
    </div>
  );
}

export default SearchPage;
