<script>
  import { link } from "svelte-spa-router";
  import fastapi from "../lib/api"
  import { page, is_login, keyword, prev_page, category } from "../lib/store"
  import moment from "moment/min/moment-with-locales"

  
  $category = "home"
  $prev_page = "/"

  let question_list = []
  let size = 10
  let total = 0
  let kw = ""
  $: total_page = Math.ceil(total / size)   // 스벨트에서 변수 앞에 `$:` 가 붙으면 `반응형 변수`

  // 질문 목록 가져오는 함수
  function get_question_list() {
    let params = {
      page: $page,
      size: size,
      keyword: $keyword
    }

    fastapi('get', '/api/questions', params, (json) => {
      question_list = json.question_list
      total = json.total
      kw = $keyword
    })
  }

  // 질문 목록 가져오기
  // $: 변수1, 변수2, 자바스크립트식 => "변수1" 또는 "변수2"의 값이 변경되면 자동으로 "자바스크립트식"을 실행
  $: $page, $keyword, get_question_list()  
</script>

<div class="container my-3">
  <h2 class="border-bottom py-2">질문과 답변</h2>
  <div class="row my-3">
    <div class="col-6">
      <a use:link href="/question-create" class="btn btn-primary {$is_login ? "" : "disabled"}">질문 등록하기</a>
    </div>
    <div class="col-6">
      <div class="input-group">
        <input type="text" class="form-control" bind:value="{kw}">
        <button class="btn btn-outline-secondary" on:click={() => {$keyword = kw, $page = 0}}>
          검색하기
        </button>
      </div>
    </div>
  </div>
  <table class="table text-center ">
    <thead>
      <tr class="table-dark">
        <th>번호</th>
        <th style="width: 50%;">제목</th>
        <th>작성자</th>
        <th>작성일시</th>
        <th>조회수</th>
      </tr>
    </thead>
    <tbody>
    {#each question_list as question}
      <tr class="text-center">
        <td>{question.id}</td>
        <td class="text-start">
          <a use:link href="/detail/{question.id}">{question.subject}</a>
          {#if question.answers.length > 0}
            <span class="text-danger small mx-2">{question.answers.length}</span>
          {/if}
        </td>
        <td>{question.user ? question.user.username : ""}</td>
        <td>{moment(question.create_date).format("YYYY년 MM월 DD일 HH:mm")}</td>
        <td>{question.hits}</td>
      </tr>
    {/each}
    </tbody>
  </table>
  <!-- 페이징 처리 시작 -->
  <ul class="pagination justify-content-center">
    <!-- 이전 페이지 -->
    <li class="page-item {$page <= 0 && 'disabled'}">
      <button class="page-link" on:click="{() => $page--}">이전</button>
    </li>
    <!-- 페이지 번호 -->
    {#each Array(total_page) as _, loop_page}
      <!-- 
          스벨트의 Array는 키, 값의 형태로 이루어짐
          근데 위의 Array(total_page)의 요소는 undefined이므로 _ 변수로 처리해주고
          값만 loop_page로 가져옴
      -->
      {#if loop_page >= $page - 5 && loop_page <= $page + 5}
        <li class="page-item {loop_page === $page && 'active'}">
          <button on:click="{() => $page = loop_page}" class="page-link">{loop_page+1}</button>
        </li>  
      {/if}
    {/each}
    <!-- 다음 페이지 -->
    <li class="page-item {$page >= total_page - 1 && 'disabled'}">
      <button class="page-link" on:click="{() => $page++}">다음</button>
    </li>
  </ul>
  <!-- 페이징 처리 끝 -->
</div>