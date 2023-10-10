// 데이터 송수신을 위한 fastapi 함수
// 공통으로 사용하기 위해 라이브러리로 따로 만둘어준거임
const fastapi = (operation, url, params, success_callback, failure_callback) => {
    let method = operation;
    let content_type = "application/json";
    let body = JSON.stringify(params);

    let _url = import.meta.env.VITE_SERVER_URL + url;
    if (method === "get") {
        // get 요청일 때
        _url += "?" + new URLSearchParams(params);
    }

    let options = {
        method: method,
        headers: {
            "Content-Type": content_type,
        },
    };

    if (method !== "get") {
        // get 요청이 아닐 때
        options['body'] = body
    }

    fetch(_url, options).then(response => {response.json()
        .then(json => {
            if (response.status >= 200 && response.status < 300) {      // 200 ~ 300
                if (success_callback) {
                    success_callback(json)
                }
            } else {
                if (failure_callback) {
                    failure_callback(json)
                } else {
                    alert(JSON.stringify(json))
                }
            }
        })
        .catch(error => {
            alert(JSON.stringify(error))
        })
    })
}
