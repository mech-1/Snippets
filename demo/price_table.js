let cost = Number(prompt("Стоимость товара: "));
let n = Number(prompt("Количество товаров: "));
// let i = 1
// while (i <= n) {
//     console.log(i, 'price =', cost * n);
//     console.log(`count = ${i}, total = ${i * cost}`);
//     i++;
// }

for (let i=1; i <= n; i++) {
    console.log(`count = ${i}, total = ${i * cost}`);
}

let fruits = ['apple','kiwi', 'banana','apricot']
fruits[6] = 'pear'
// 2 undefined
console.log(fruits)

for (let fruit of fruits){
    // apple, kiwi, ...
    console.log(fruit);
}
for (let fruit in fruits){
    // 0, 1, 2, 3
    console.log(fruit)
}

let people = {
    name: 'Ivan',
    age: 34,
    salary: 2000
}

for (let param in people) {
    console.log(param)
//     show keys
}
// from object create iterable
// get values from object people
Object.values(people);
// get keys from object
Object.keys(people)


// for ... of only for iterable objects (string, array, map)
for (let value of Object.values(people)) {
    console.log(value)
//     show keys
}
let names = ['Alex','Olga','Anna']
for (let value in names){
    // get index 0,1,2,...
    console.log(value)
}