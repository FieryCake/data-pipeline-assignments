//Source for setting up 
//https://s55ma.radioamater.si/2023/05/30/ubuntu-22-04-install-puppeteer/
const puppeteer = require('puppeteer');
const fs = require('fs');
const AWS = require('aws-sdk');

var s3 = new AWS.S3();
var results = []
const params = {
    Bucket: 'assignment1bucket-glenn',
    Key: 'output/cleanedData.json'
  };

s3.getObject(params, function(err, data) {
if (err) console.log(err, err.stack);
else {
    // fs.writeFileSync('output.json', data.Body.toString());
    var jsonObject = data.Body.toString();
    jsonObject = jsonObject.split("\n")
    links = []
    for (const i of jsonObject){
        links.push(JSON.parse(i).link)
    }
    console.log(jsonObject.length);
    console.log("Successfully downloaded data from S3");
    run(jsonObject);
}
});


async function run (ob) {
  const browser = await puppeteer.launch({
    executablePath: '/usr/bin/google-chrome-stable',
    args: ['--no-sandbox'],
    defaultViewport: {width: 1920, height: 1080}
  });

  const page = await browser.newPage();
  var counter = 0;
//   li = ['https://www.huffpost.com/entry/covid-boosters-uptake-us_n_632d719ee4b087fae6feaac9','https://www.huffpost.com/entry/covid-boosters-uptake-us_n_632d719ee4b087fae6feaac9']
  for (const link of links) {
    const page = await browser.newPage();

    let timeout;
    const timeoutPromise = new Promise((_, reject) => {
        timeout = setTimeout(() => {
            reject(new Error('Timeout exceeded'));
        }, 4000);
    });

    try {
        const response = await Promise.race([
            page.goto(link, { waitUntil: 'domcontentloaded' }),
            await new Promise(resolve => setTimeout(resolve, 1800)),
            timeoutPromise
        ]);

        const textContent = await page.evaluate(() => {
            const spanElement = document.evaluate("//span[@class='view-comments-button--count'][1]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;

            return spanElement ? spanElement.textContent : 'Element not found';
        });

        console.log(textContent);
        const jsonObject = JSON.parse(ob[counter]);
        jsonObject.comment = textContent
        results.push(jsonObject);
        fs.writeFileSync('scraped.json', JSON.stringify(results)+ "\n");
    } catch (error) {
        console.error(`Error occurred for link: ${link}`, error);
    } finally {
        clearTimeout(timeout);
        await page.close();
        counter+=1
    }
}

  browser.close();
  
}


function sleep(ms) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
} 