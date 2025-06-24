const express=require("express");
const ejs=require("ejs");//view engine
const path=require("path");
const fs = require('fs');

const folder_path=path.join(__dirname,"/data"); 
const urls_file=fs.readFileSync(path.join(folder_path,"problems_url.txt"), 'utf-8');
const urls = urls_file
  .trim()
  .split('\n')
  .map(line => line.trim());
const titles_file=fs.readFileSync(path.join(folder_path,"problems_title.txt"), 'utf-8');
const titles = titles_file
  .trim()
  .split('\n')
  .map(line => line.trim());
const difficulty_file=fs.readFileSync(path.join(folder_path,"difficulty_data.txt"), 'utf-8');
const difficulty = difficulty_file
  .trim()
  .split('\n')
  .map(line => line.trim());
const acceptance_file=fs.readFileSync(path.join(folder_path,"acceptance.txt"), 'utf-8');
const acceptance = acceptance_file
  .trim()
  .split('\n')
  .map(line => line.trim());

const IDF_file = fs.readFileSync(path.join(folder_path,"IDF.txt"), 'utf-8');
const IDF= IDF_file
  .trim()
  .split('\n')
  .map(Number);
const TFIDF_file = fs.readFileSync(path.join(folder_path,"TFIDF.txt"), 'utf-8');
const TFIDF = TFIDF_file
  .trim()
  .split('\n')
  .map(line => {
    const [docIdx, wordIdx, value] = line.trim().split(/\s+/).map(Number);
    return [docIdx, wordIdx, value];
  });
const Magnitude_file = fs.readFileSync(path.join(folder_path,"Magnitude.txt"), 'utf-8');
const Magnitude= Magnitude_file
  .trim()
  .split('\n')
  .map(Number);
const Keywords_file = fs.readFileSync(path.join(folder_path,"keyword.txt"), 'utf-8');
const Keywords = Keywords_file
  .trim()
  .split('\n')
  .map(line => line.trim());
const N=1078;
const W=9525;
const problems_des = [];
const new_folder_path=path.join(folder_path,"/problems_desc");
for (let i = 1; i <= 1078; i++) {
  const filePath = path.join(new_folder_path, `problem${i}.txt`);
  const content = fs.readFileSync(filePath, 'utf-8').trim();
  problems_des.push(content);
}
const docVectors = new Map();
for (const [docIdx, wordIdx, value] of TFIDF) {
  if (!docVectors.has(docIdx)) docVectors.set(docIdx, new Map());
  docVectors.get(docIdx).set(wordIdx, value);
}


const PORT=process.env.PORT||3000;
const app=express();


app.set("view engine","ejs");
app.use(express.static(path.join(__dirname,"/public")));
app.use(express.json());


app.get("/",(req,res)=>{
    res.render("index");
})

app.get("/search",(req,res)=>{
    const rawQuery = req.query.question;
    if (!rawQuery) return res.status(400).send("Missing query parameter");
    const query = rawQuery.toLowerCase().trim();
    const tokens = query.split(/\s+/); // tokenize query
    const query_tf = {}; // raw frequency
    for (let token of tokens) {
        if (!Keywords.includes(token)) continue;
        query_tf[token] = (query_tf[token] || 0) + 1;
    }
    const query_vector = new Array(W).fill(0);
    let query_magnitude = 0;

    for (let [term, tf] of Object.entries(query_tf)) {
        const index = Keywords.indexOf(term);
        const tfidf = tf * IDF[index];
        query_vector[index] = tfidf;
        query_magnitude += tfidf * tfidf;
    }
    query_magnitude = Math.sqrt(query_magnitude);

    // compute cosine similarity
    const results = [];
    for (let [docIndex, wordMap] of docVectors.entries()) {
        let dot = 0;
        for (let [wordIndex, tfidf] of wordMap.entries()) {
            dot += tfidf * query_vector[wordIndex];
        }
        const denom = Magnitude[docIndex] * query_magnitude;
        const similarity = denom === 0 ? 0 : dot / denom;
        if (similarity > 0) {
            results.push({ docIndex, similarity });
        }
    }
    // sort and send top 10
    results.sort((a, b) => b.similarity - a.similarity);
    const topResults = results.slice(0, 10);
    const allZero = topResults.every(item => item.similarity === 0);
    if (allZero || topResults.length === 0) {
      return res.json({ message: "No adequate match" });
    }
    const topDocIndices = topResults.map(item => item.docIndex);
    const response = topDocIndices.map(docIndex => ({
      id:docIndex,  
      url: urls[docIndex],
      title:titles[docIndex],
      problem_desc: problems_des[docIndex],
      acceptance: acceptance[docIndex],
      difficulty: difficulty[docIndex],
    }));
    res.json(response);
})

app.get("/problems/:id", (req, res) => {
  const id = parseInt(req.params.id);
   res.render("problem", {
    url: urls[id],
    title: titles[id],
    problem_desc: problems_des[id],
    acceptance: acceptance[id],
    difficulty: difficulty[id],
  });
})

app.listen(PORT,()=>{
    console.log("Server is running on Port : " + PORT);
})