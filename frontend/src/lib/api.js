import qs from "qs"
import { access_token, username, is_login } from "./store"
import { get } from "svelte/store";
import { push } from "svelte-spa-router";

// 데이터 송수신을 위한 fastapi 함수
// 공통으로 사용하기 위해 라이브러리로 따로 만둘어준거임
const fastapi = (operation, url, params, success_callback, failure_callback) => {
    let method = operation;
    let content_type = "application/json";
    let body = JSON.stringify(params);

    // 로그인 요청일 경우
    if (operation === "login") {
        method = "post"
        content_type = "application/x-www-form-urlencoded"  // OAuth2를 사용하여 로그인을 할 때는 Content-Type이 'application/x-www-form-urlencoded'이어야 함
        body = qs.stringify(params) // params 데이터를 'application/x-www-form-urlencoded' 형식에 맞게끔 변환
    }

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
    }

    // 스토어 변수인 access_token에 값이 있을 경우에 HTTP 헤더에 Authorization 항목을 추가
    const _access_token = get(access_token)     // 스토어 변수의 값을 읽기 위해 get 함수를 사용함
    if (_access_token) {
        options.headers["Authorization"] = "Bearer " + _access_token
    }

    if (method !== "get") {
        // get 요청이 아닐 때
        options['body'] = body
    }

    fetch(_url, options)
        .then(response => {
            if (response.status === 204) {      // No content
                if (success_callback) {
                    success_callback()
                }
                return
            }
            response.json()
                .then(json => {
                    if (response.status >= 200 && response.status < 300) {      // 200 ~ 300
                        if (success_callback) {
                            success_callback(json)
                        }
                    } 

                    // operation이 'login'이 아니고 401 오류가 발생한 경우는 '로그인이 필요한 상황'
                    // 유효기간이 종료된 토큰을 사용할 경우에도 401 오류가 발생
                    else if (operation !== "login" && response.status === 401) {
                        access_token.set("")
                        username.set("")
                        is_login.set(false)
                        alert("로그인이 필요합니다.")
                        push("/user-login")
                    } 
                    
                    else {
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

export default fastapi