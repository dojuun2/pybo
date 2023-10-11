<script>
  import { link } from "svelte-spa-router";
  import fastapi from "../lib/api"
  let question_list = [];

  // 질문 목록 가져오는 함수
  function get_question_list() {
    fastapi('get', '/api/question/list', {}, (json) => {
      question_list = json
    })
  }

  // 질문 목록 가져오기
  get_question_list()
</script>

<ul>
  {#each question_list as question}
    <li><a use:link href="/detail/{question.id}">{question.subject}</a></li>
  {/each}
</ul>
