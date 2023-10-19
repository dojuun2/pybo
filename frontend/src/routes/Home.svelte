<script>
  import { link } from "svelte-spa-router";
  import fastapi from "../lib/api"
  import { page, is_login } from "../lib/store"
  import moment from "moment/min/moment-with-locales"

  let question_list = []
  let size = 10
  let total = 0
  $: total_page = Math.ceil(total / size)   // 스벨트에서 변수 앞에 `$:` 가 붙으면 `반응형 변수`
  
  // 질문 목록 가져오는 함수
  function get_question_list(_page) {
    let params = {
      page: _page,
      size: size,
    }

    fastapi('get', '/api/question/list', params, (json) => {
      question_list = json.question_list
      $page = _page     // $page: 스토어 변수 -> store.js 파일에 있는 page 변수
      total = json.total
    })
  }

  // 질문 목록 가져오기
  $: get_question_list($page)   // page 값이 변경될 경우 get_question_list() 함수도 다시 호출하라는 의미
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
    {#each question_list as question}
      <tr>
        <td>{question.id}</td>
        <td>
          <a use:link href="/detail/{question.id}">{question.subject}</a>
          {#if question.answers.length > 0}
            <span class="text-danger small mx-2">{question.answers.length}</span>
          {/if}
        </td>
        <td>{moment(question.create_date).format("YYYY년 MM월 DD일 HH:mm")}</td>
      </tr>
    {/each}
    </tbody>
  </table>
  <!-- 페이징 처리 시작 -->
  <ul class="pagination justify-content-center">
    <!-- 이전 페이지 -->
    <li class="page-item {$page <= 0 && 'disabled'}">
      <button class="page-link" on:click="{() => get_question_list($page-1)}">이전</button>
    </li>
    <!-- 페이지 번호 -->
    {#each Array(total_page) as _, loop_page}
      {#if loop_page >= $page - 5 && loop_page <= $page + 5}
        <li class="page-item {loop_page === $page && 'active'}">
          <button on:click="{() => get_question_list(loop_page)}" class="page-link">{loop_page+1}</button>
        </li>  
      {/if}
    {/each}
    <!-- 다음 페이지 -->
    <li class="page-item {$page >= total_page - 1 && 'disabled'}">
      <button class="page-link" on:click="{() => get_question_list($page+1)}">다음</button>
    </li>
  </ul>
  <!-- 페이징 처리 끝 -->
  <a use:link href="/question-create" class="btn btn-primary {$is_login ? "" : "disabled"}">질문 등록하기</a>
</div>