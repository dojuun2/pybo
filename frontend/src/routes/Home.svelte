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

<div class="container my-3">
  <table class="table">
    <thead>
      <tr class="table-dark">
        <th>번호</th>
        <th>제목</th>
        <th>작성일시</th>
      </tr>
    </thead>
    <tbody>
    {#each question_list as question, i}
      <tr>
        <td>{i+1}</td>
        <td>
          <a use:link href="/detail/{question.id}">{question.subject}</a>
        </td>
        <td>{question.create_date}</td>
      </tr>
    {/each}
    </tbody>
  </table>
  <a use:link href="/question-create" class="btn btn-primary">질문 등록하기</a>
</div>