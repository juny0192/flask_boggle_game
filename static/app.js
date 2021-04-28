const $guessInput = $("#guessInp");
const $guessSubmit = $("#guessSubmit");
const $result = $("#result");

// class BoggleGame {

//     constructor(boardID)

// }

$guessSubmit.on("click", async function (evt) {
  evt.preventDefault();

  let searchVal = $guessInput.val();
  if (searchVal.length === 0) {
    return;
  }

  const res = await axios.get("/check", { params: { q: searchVal } });

  if (res.data.result === "not-word") {
    showMessage(`${searchVal} is not a valid English word`);
  } else if (res.data.result === "not-on-board") {
    showMessage(`${searchVal} is not a valid English but not on the board`);
  } else {
    showMessage(`Added: ${searchVal}`);
    $result.append($("<li>"), { searchVal });
  }

  $result.val("");
});

function showMessage(msg) {
  $("#msg").text(msg);
}
