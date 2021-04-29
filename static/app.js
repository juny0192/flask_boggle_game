const $guessInput = $("#guessInp");
const $guessSubmit = $("#guessSubmit");
const $result = $("#result");
const $submitForm = $("#submit-form");

wordStorage = new Set();
let total = 0;
let time = 60;

function showMessage(msg) {
  $("#msg").text(msg);
}

function showScore(score) {
  $("#score").text(score);
}

let countTime = setInterval(function () {
  time -= 1;
  showTimer();
  if (time === 0) {
    clearInterval(countTime);
    $submitForm.hide();
    endGame();
  }
}, 1000);

function showTimer() {
  $("#timer").text(`Time left: ${time}`);
}

$guessSubmit.on("click", clickHandler);

async function clickHandler(evt) {
  evt.preventDefault();

  let searchVal = $guessInput.val();

  if (searchVal.length === 0) {
    showMessage(`You need to enter any valid word.`);
    return;
  }

  if (wordStorage.has(`${searchVal}`)) {
    showMessage(`You found the word: "${searchVal}" already.`);
    return;
  }

  const res = await axios.get("/check", { params: { q: searchVal } });

  if (res.data.result === "not-word") {
    showMessage(`"${searchVal}" is not a valid English word`);
  } else if (res.data.result === "not-on-board") {
    showMessage(`"${searchVal}" is not a valid English but not on the board`);
  } else {
    showMessage(`Added: "${searchVal}"`);
    $result.prepend($(`<li class="list-group-item">${searchVal}</li>`));
    wordStorage.add(`${searchVal}`);
    total += searchVal.length;
  }

  $guessInput.val("");
}

async function endGame() {
  const res = await axios.post("/post-score", { score: total });

  if (res.data.newRecord === true) {
    showMessage(`New record is '${total}'`);
  } else {
    showMessage(`Final score is '${total}'`);
  }
}
