import {handler} from "./index"

console.log('?')

// @ts-ignore
handler({
    headers: {
        "content-type": "application/x-www-form-urlencoded"
    },
    body: "name=test&url=https%3A%2F%2Ftools.jongwoo.me&keywords=&requestBy="
} )
