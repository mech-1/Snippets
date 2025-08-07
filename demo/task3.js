const data = { a: 5, b: 2, c: 3 };

function sumObjectValues(data) {
    let sumNumbers = 0;
    for (let number of Object.values(data)) {
        sumNumbers += number;
    }
  return sumNumbers;
}

console.log(sumObjectValues(data));
