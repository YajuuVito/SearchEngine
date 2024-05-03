# SearchEngine
Repo of CSIT5930 course project

![alt text](image.png)

# Use Search Engine Directly (needn't crawler)
1. install python requirements
   ```
    pip install -r requirements.txt
   ```
2. start backend server
   ```
    cd backend
    python manage.py runserver
   ```
3. open `build/index.html` in browser to use our search engine

# Start From Crawler
1. install python requirements
   ```
    pip install -r requirements.txt
   ```
2. run `crawler/crawler.py` to get data from ust server.
   ```
   cd crawler
   python crawler.py
   ```
3. data pre-processing, run scripts in folder `index`.
   ```
   cd ../index
   python indexing.py
   python inverted_index.py
   python pageRank.py
   python idf.py
   python tf.py
   ```
4. move data to `backend\SE\data` 
   - adj_matrix.json
   - data.json
   - idf.json
   - index.json
   - inverted_index.json
   - page_rank.json
   - tf_idf.json
   - tf.json
5. start backend server
   ```
    cd backend
    python manage.py runserver
   ```
6. open `build/index.html` in browser to use our search engine
