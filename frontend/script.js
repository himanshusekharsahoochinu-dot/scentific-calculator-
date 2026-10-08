/* =====================================
   BACKEND URL
===================================== */

const API_URL =
    "http://127.0.0.1:5000";


/* =====================================
   ELEMENTS
===================================== */

const display =
    document.getElementById("display");


const previousDisplay =
    document.getElementById(
        "previous-display"
    );


const historyContainer =
    document.getElementById(
        "history"
    );


const degreeButton =
    document.getElementById(
        "degree-btn"
    );


const radianButton =
    document.getElementById(
        "radian-btn"
    );


/* =====================================
   MODE
===================================== */

let angleMode = "DEG";


/* =====================================
   ADD VALUE
===================================== */

function appendValue(value) {

    if (display.value === "0") {

        display.value = value;

    } else {

        display.value += value;

    }

}


/* =====================================
   ADD FUNCTION
===================================== */

function appendFunction(functionName) {

    if (display.value === "0") {

        display.value = functionName;

    } else {

        display.value += functionName;

    }

}


/* =====================================
   ADD OPERATOR
===================================== */

function appendOperator(operator) {

    if (display.value === "0") {

        if (operator === "-") {

            display.value = "-";

        }

        return;

    }

    display.value += operator;

}


/* =====================================
   CLEAR DISPLAY
===================================== */

function clearDisplay() {

    display.value = "0";

    previousDisplay.textContent = "";

}


/* =====================================
   DELETE
===================================== */

function deleteLast() {

    if (
        display.value.length <= 1
    ) {

        display.value = "0";

    } else {

        display.value =
            display.value.slice(
                0,
                -1
            );

    }

}


/* =====================================
   DEGREE MODE
===================================== */

degreeButton.addEventListener(
    "click",
    function () {

        angleMode = "DEG";

        degreeButton.classList.add(
            "active"
        );

        radianButton.classList.remove(
            "active"
        );

    }
);


/* =====================================
   RADIAN MODE
===================================== */

radianButton.addEventListener(
    "click",
    function () {

        angleMode = "RAD";

        radianButton.classList.add(
            "active"
        );

        degreeButton.classList.remove(
            "active"
        );

    }
);


/* =====================================
   CALCULATE
===================================== */

async function calculate() {

    const expression =
        display.value.trim();


    if (!expression) {

        return;

    }


    try {

        const response =
            await fetch(
                `${API_URL}/api/calculate`,
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body: JSON.stringify({

                        expression:
                            expression,

                        mode:
                            angleMode

                    })

                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Calculation failed."
            );

        }


        previousDisplay.textContent =
            `${expression} =`;


        display.value =
            data.result;


        loadHistory();

    }


    catch (error) {

        console.error(error);

        previousDisplay.textContent =
            "Error";

        display.value =
            "Error";

    }

}


/* =====================================
   LOAD HISTORY
===================================== */

async function loadHistory() {

    try {

        const response =
            await fetch(
                `${API_URL}/api/history`
            );


        const data =
            await response.json();


        if (!data.success) {

            return;

        }


        historyContainer.innerHTML =
            "";


        data.history.forEach(
            function (item) {

                const div =
                    document.createElement(
                        "div"
                    );


                div.className =
                    "history-item";


                div.textContent =
                    `${item.expression} = ${item.result} [${item.mode}]`;


                div.addEventListener(
                    "click",
                    function () {

                        display.value =
                            item.result;

                    }
                );


                historyContainer.appendChild(
                    div
                );

            }
        );

    }


    catch (error) {

        console.error(
            "History error:",
            error
        );

    }

}


/* =====================================
   CLEAR HISTORY
===================================== */

async function clearHistory() {

    try {

        const response =
            await fetch(
                `${API_URL}/api/history`,
                {
                    method: "DELETE"
                }
            );


        const data =
            await response.json();


        if (data.success) {

            historyContainer.innerHTML =
                "";

        }

    }


    catch (error) {

        console.error(
            "Clear history error:",
            error
        );

    }

}


/* =====================================
   KEYBOARD SUPPORT
===================================== */

document.addEventListener(
    "keydown",
    function (event) {

        const key = event.key;


        if (
            key >= "0" &&
            key <= "9"
        ) {

            appendValue(key);

        }


        else if (
            key === "." ||
            key === "(" ||
            key === ")"
        ) {

            appendValue(key);

        }


        else if (
            key === "+" ||
            key === "-" ||
            key === "*" ||
            key === "/" ||
            key === "^"
        ) {

            appendOperator(key);

        }


        else if (
            key === "Enter" ||
            key === "="
        ) {

            event.preventDefault();

            calculate();

        }


        else if (
            key === "Backspace"
        ) {

            deleteLast();

        }


        else if (
            key === "Escape"
        ) {

            clearDisplay();

        }

    }
);


/* =====================================
   LOAD HISTORY AT START
===================================== */

loadHistory();