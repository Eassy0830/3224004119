#!/usr/bin/env node
/* 小学四则运算题目生成与判题程序。Node.js 18+，无第三方依赖。 */
const fs = require('fs');

const gcd = (a, b) => { a = a < 0n ? -a : a; b = b < 0n ? -b : b; while (b) [a, b] = [b, a % b]; return a; };
class Rat {
  constructor(n, d = 1n) { if (d === 0n) throw Error('分母不能为零'); if (d < 0n) [n, d] = [-n, -d]; const g = gcd(n, d); this.n = n / g; this.d = d / g; }
  add(x) { return new Rat(this.n * x.d + x.n * this.d, this.d * x.d); }
  sub(x) { return new Rat(this.n * x.d - x.n * this.d, this.d * x.d); }
  mul(x) { return new Rat(this.n * x.n, this.d * x.d); }
  div(x) { return new Rat(this.n * x.d, this.d * x.n); }
  cmp(x) { const z = this.n * x.d - x.n * this.d; return z < 0n ? -1 : z > 0n ? 1 : 0; }
  key() { return `${this.n}/${this.d}`; }
  text() { if (this.d === 1n) return String(this.n); const w = this.n / this.d, r = this.n % this.d; return w === 0n ? `${r}/${this.d}` : `${w}’${r}/${this.d}`; }
}
const zero = new Rat(0n), OPS = ['+', '-', '×', '÷'], prec = { '+': 1, '-': 1, '×': 2, '÷': 2 };
class Expr {
  constructor(value, op = null, left = null, right = null) { Object.assign(this, { value, op, left, right }); }
  operators() { return this.op ? 1 + this.left.operators() + this.right.operators() : 0; }
  canonical() { if (!this.op) return `n:${this.value.key()}`; let a = this.left.canonical(), b = this.right.canonical(); if ((this.op === '+' || this.op === '×') && b < a) [a, b] = [b, a]; return `${this.op}(${a},${b})`; }
  render(parent = null, right = false) { if (!this.op) return this.value.text(); const s = `${this.left.render(this.op, false)} ${this.op} ${this.right.render(this.op, true)}`; return parent && (prec[this.op] < prec[parent] || (right && prec[this.op] === prec[parent])) ? `(${s})` : s; }
}
const leaf = x => new Expr(x);
function combine(op, a, b) {
  let v;
  if (op === '+') v = a.value.add(b.value);
  else if (op === '-') { if (a.value.cmp(b.value) < 0) return null; v = a.value.sub(b.value); }
  else if (op === '×') v = a.value.mul(b.value);
  else { if (b.value.cmp(zero) === 0) return null; v = a.value.div(b.value); if (v.cmp(zero) <= 0 || v.cmp(new Rat(1n)) >= 0) return null; }
  return new Expr(v, op, a, b);
}
class Generator {
  constructor(r, random = Math.random) { if (!Number.isInteger(r) || r < 1) throw Error('-r 必须是大于等于 1 的自然数'); this.r = r; this.random = random; }
  int(n) { return Math.floor(this.random() * n); }
  randomLeaf() { if (this.r === 1 || this.random() < .55) return leaf(new Rat(BigInt(this.int(this.r)))); const d = 2 + this.int(this.r - 2), n = 1 + this.int(d - 1); return leaf(new Rat(BigInt(n), BigInt(d))); }
  expr(count) { if (!count) return this.randomLeaf(); const leftCount = this.int(count), rightCount = count - 1 - leftCount; for (let i = 0; i < 80; i++) { const x = this.expr(leftCount), y = this.expr(rightCount), e = combine(OPS[this.int(4)], x, y); if (e) return e; } return null; }
  generate(amount) { if (!Number.isInteger(amount) || amount < 1) throw Error('-n 必须是大于等于 1 的自然数'); const all = [], seen = new Set(), limit = Math.max(10000, amount * 300); for (let i = 0; i < limit; i++) { const e = this.expr(1 + this.int(3)); if (e && !seen.has(e.canonical())) { seen.add(e.canonical()); all.push(e); if (all.length === amount) return all; } } throw Error(`在 -r ${this.r} 的可用表达式空间内未能生成 ${amount} 道不重复题目；请增大 -r 或减小 -n。`); }
}
function number(text) { text = text.replace('’', "'"); let n, d; if (text.includes("'")) { const [w, f] = text.split("'"); [n, d] = f.split('/'); return new Rat(BigInt(w) * BigInt(d) + BigInt(n), BigInt(d)); } if (text.includes('/')) { [n, d] = text.split('/'); return new Rat(BigInt(n), BigInt(d)); } return new Rat(BigInt(text)); }
function tokens(s) { const re = /\s*(\d+(?:['’]\d+\/\d+|\/\d+)?|[+\-×*÷/]|[()])/gy, out = []; let p = 0, m; while (p < s.length) { re.lastIndex = p; m = re.exec(s); if (!m) { if (/^\s*$/.test(s.slice(p))) break; throw Error(`无法识别的字符：${s.slice(p)}`); } out.push(m[1]); p = re.lastIndex; } return out; }
function parse(s) { const t = tokens(s); let i = 0; const atom = () => { const x = t[i++]; if (x === '(') { const e = add(); if (t[i++] !== ')') throw Error('括号不匹配'); return e; } if (!x || OPS.includes(x) || x === ')') throw Error('缺少数字'); return leaf(number(x)); }; const mul = () => { let a = atom(); while (['×','*','÷','/'].includes(t[i])) { let op = t[i++]; op = op === '*' ? '×' : op === '/' ? '÷' : op; const z = combine(op, a, atom()); if (!z) throw Error('不合法的除法'); a = z; } return a; }; const add = () => { let a = mul(); while (['+','-'].includes(t[i])) { const z = combine(t[i++], a, mul()); if (!z) throw Error('减法产生负数'); a = z; } return a; }; const e = add(); if (i !== t.length) throw Error('表达式末尾有多余内容'); return e; }
function entries(file) { const map = new Map(); fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, '').split(/\r?\n/).forEach(x => { const m = x.match(/^\s*(\d+)\.\s*(.*?)\s*$/); if (m) map.set(+m[1], m[2]); }); return map; }
function generate(n, r) { const ex = new Generator(r).generate(n); fs.writeFileSync('Exercises.txt', ex.map((e,i) => `${i+1}. ${e.render()} =`).join('\n') + '\n'); fs.writeFileSync('Answers.txt', ex.map((e,i) => `${i+1}. ${e.value.text()}`).join('\n') + '\n'); }
function grade(eFile, aFile) { const e = entries(eFile), a = entries(aFile), ok = [], bad = []; [...e.keys()].sort((x,y)=>x-y).forEach(k => { try { const expected = parse(e.get(k).replace(/=\s*$/, '').trim()).value, actual = number(a.get(k) || ''); (expected.cmp(actual) === 0 ? ok : bad).push(k); } catch (_) { bad.push(k); } }); const line = (n, xs) => `${n}: ${xs.length} (${xs.join(', ')})`; fs.writeFileSync('Grade.txt', `${line('Correct',ok)}\n${line('Wrong',bad)}\n`); }
function main(args) { const get = flag => { const i = args.indexOf(flag); return i < 0 ? null : args[i+1]; }; if (args.includes('-h') || args.includes('--help') || !args.length) { console.log('用法：node Myapp.js -n COUNT -r RANGE\n      node Myapp.js -e EXERCISES.txt -a ANSWERS.txt'); return; } try { const n = get('-n'), r = get('-r'), e = get('-e'), a = get('-a'); if (n !== null) { if (r === null || e !== null || a !== null) throw Error('生成模式用法：-n COUNT -r RANGE'); generate(Number(n), Number(r)); console.log(`已生成 ${n} 道题目：Exercises.txt 和 Answers.txt`); } else { if (e === null || a === null || r !== null) throw Error('判题模式用法：-e EXERCISES.txt -a ANSWERS.txt'); grade(e,a); console.log('判题完成：Grade.txt'); } } catch (err) { console.error(`错误：${err.message}`); process.exitCode = 2; } }
if (require.main === module) main(process.argv.slice(2));
module.exports = { Rat, Expr, Generator, combine, leaf, number, parse, generate, grade };
