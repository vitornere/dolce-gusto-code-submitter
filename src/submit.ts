// submitCodes.js
import fs from 'fs';
import { CookieJar } from 'tough-cookie';
import got from 'got';
import { JSDOM } from 'jsdom';
import { codes } from './codes.js';

// 1️⃣ Prepare your cookie jar from your exported browser cookies
// session.json is an array of { name, value, domain, path, … } or at least { name, value } pairs
const jar = new CookieJar();
const cookies = JSON.parse(fs.readFileSync('session.json', 'utf8'));
for (const ck of cookies) {
    // adjust the URL to match the cookie’s domain/path
    jar.setCookieSync(
        `${ck.name}=${ck.value}; Domain=${ck.domain || 'nescafe-dolcegusto.com.br'}; Path=${ck.path || '/'}`,
        'https://www.nescafe-dolcegusto.com.br'
    );
}
console.log(cookies)

// 2️⃣ Create a got instance that reuses your cookies
const client = got.extend({
    cookieJar: jar,
    headers: {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7,es;q=0.6",
        "Priority": "u=0, i",
        "Sec-Ch-Ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"macOS\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        'Sec-Fetch-Site': 'same-origin',
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    },
});

// 3️⃣ Fetch the “enter code” page to grab the fresh form_key
async function getFormKey() {
    const res = await client.get('https://www.nescafe-dolcegusto.com.br/club');
    const dom = new JSDOM(res.body);
    const input = dom.window.document.querySelector('input[name="form_key"]');
    if (!input) throw new Error('form_key not found');
    return input.value;
}

// 4️⃣ Loop over your codes
async function submitCodes(codes) {
    const formKey = await getFormKey();
    console.log(formKey);
    for (const code of codes) {
        const resp = await client.post('https://www.nescafe-dolcegusto.com.br/club/code/add/', {
            form: { form_key: formKey, code }
        });
        console.log(code, '→', resp.statusCode, resp.body.slice(0, 200));

        // **throttle**: wait 10–30 seconds before next code
        await new Promise(resolve => setTimeout(resolve, Math.random() * 20000 + 10000));
    }
}

submitCodes(codes).catch(console.error);
