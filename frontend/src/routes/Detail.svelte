<script>
    import fastapi from "../lib/api";

    export let params = {}
    let question_id = params.question_id
    let question = {answers:[]}
    let content = ""

    function get_question() {
        fastapi("get", "/api/question/detail/" + question_id, {}, (json) => {
            question = json
        })
    }

    get_question()

    function post_answer(event) {
        event.preventDefault()  // submit이 눌릴경우 form이 자동으로 전동되는 것을 방지하기 위함
        
        let url = "/api/answer/create/" + question_id
        let params = {
            content: content,
        }
        fastapi('post', url, params, (json) => {
            content = ''
            get_question()
        })
    }
</script>
<h1>{question.subject}</h1>
<div>
    {question.content}
</div>
<ul>
    {#each question.answers as answer}
        <li>{answer.content}</li>
    {/each}
</ul>
<form method="post">
    <textarea rows="15" bind:value={content}></textarea>
    <input type="submit" value="답변등록" on:click={post_answer}>
</form>