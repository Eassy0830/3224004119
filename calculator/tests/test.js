const assert = require('assert'), fs = require('fs'), os = require('os'), path = require('path');
const { Rat, Generator, combine, leaf, number, parse, grade } = require('../Myapp');
let passed = 0; function test(name, fn) { fn(); passed++; console.log(`✓ ${name}`); }
test('分数格式', () => { assert.equal(new Rat(3n,5n).text(),'3/5'); assert.equal(new Rat(19n,8n).text(),'2’3/8'); });
test('分数加法', () => assert.equal(parse('1/6 + 1/8').value.text(), '7/24'));
test('优先级', () => assert.equal(parse('1 + 2 × 3').value.text(), '7'));
test('括号', () => assert.equal(parse('(1 + 2) × 3').value.text(), '9'));
test('禁止负数', () => assert.equal(combine('-',leaf(new Rat(1n)),leaf(new Rat(2n))),null));
test('除法真分数', () => { assert.equal(combine('÷',leaf(new Rat(4n)),leaf(new Rat(2n))),null); assert.equal(combine('÷',leaf(new Rat(1n)),leaf(new Rat(2n))).value.text(),'1/2'); });
test('交换律去重', () => assert.equal(parse('3 + (2 + 1)').canonical(), parse('1 + 2 + 3').canonical()));
test('不使用结合律', () => assert.notEqual(parse('1 + 2 + 3').canonical(), parse('3 + 2 + 1').canonical()));
test('生成约束', () => { const xs = new Generator(10, (() => { let x=1; return () => (x=(x*16807)%2147483647)/2147483647; })()).generate(100); assert.equal(new Set(xs.map(x=>x.canonical())).size,100); assert(xs.every(x=>x.operators()<=3)); });
test('判题报告', () => { const d=fs.mkdtempSync(path.join(os.tmpdir(),'math-')); fs.writeFileSync(path.join(d,'e.txt'),'1. 1/6 + 1/8 =\n2. 3 - 1 =\n'); fs.writeFileSync(path.join(d,'a.txt'),'1. 7/24\n2. 1\n'); const old=process.cwd(); process.chdir(d); grade('e.txt','a.txt'); process.chdir(old); const s=fs.readFileSync(path.join(d,'Grade.txt'),'utf8'); assert(s.includes('Correct: 1 (1)')); assert(s.includes('Wrong: 1 (2)')); });
console.log(`\n${passed} tests passed.`);
