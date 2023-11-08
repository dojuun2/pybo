<script>
  import Router from 'svelte-spa-router'
  import Home from './routes/Home.svelte'
  import Detail from './routes/Detail.svelte'
  import QuestionCreate from './routes/QuestionCreate.svelte'
  import UserCreate from './routes/UserCreate.svelte'
  import UserLogin from './routes/UserLogin.svelte'
  import QuestionModify from './routes/QuestionModify.svelte'
  import AnswerModify from './routes/AnswerModify.svelte'
  import Board from './routes/Board.svelte'
  import BoardDetail from './routes/BoardDetail.svelte'
  import BoardModify from './routes/BoardModify.svelte'
  import BoardCreate from './routes/BoardCreate.svelte'

  import Navigation from './components/Navigation.svelte';
  import SideBar from './components/SideBar.svelte';

  const routes = {
    '/': Home,
    '/detail/:question_id': Detail,
    '/question-create': QuestionCreate,
    '/user-create': UserCreate,
    '/user-login': UserLogin,
    '/question-modify/:question_id': QuestionModify,
    '/answer-modify/:answer_id': AnswerModify,
    '/board': Board,
    '/board-detail/:board_id': BoardDetail,
    '/board-modify/:board_id': BoardModify,
    '/board-create': BoardCreate,
  }
</script>

<Navigation />
<div class="d-flex">
  <SideBar />
  <Router {routes} />
</div>