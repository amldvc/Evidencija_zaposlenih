import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:5000/api', // Putanja do tvog Flask API-ja
  timeout: 1000,
  headers: { 'Content-Type': 'application/json' }
});

export default instance;
