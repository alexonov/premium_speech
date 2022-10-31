const translate = require('google-translate-extended-api');

const word = process.argv[2]; // first argument is the word to be translated
// const pos = process.argv[3]; // second argument is part of speech: noun, adjective, verb, adverb

translate(
    word,
    "en",
    "de",
    {
        examples: false,
        detailedTranslationsSynonyms: true,
        definitionSynonyms: true,
        definitionExamples: true
    }).then((res) => {
    console.log(JSON.stringify(res, undefined, 2));
}).catch(console.log);