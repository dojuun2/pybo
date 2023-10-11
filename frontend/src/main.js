import './app.css'
import App from './App.svelte'

// 부트스트랩 적용
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap/dist/js/bootstrap.min.js"


const app = new App({
  target: document.getElementById('app'),
})

export default app
