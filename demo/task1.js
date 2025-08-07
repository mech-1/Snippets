// python
// item_color
// js
// CamelCase itemColor

function findLongestWord(words) {
    let longestWord = words[0]
    for (let word of words){
        if (word.length > longestWord.length){
            longestWord = word
        }
    }
    return longestWord
}

const words = ["apple", "banana", "kiwi", "grapefruit"];
console.log(findLongestWord(words));
