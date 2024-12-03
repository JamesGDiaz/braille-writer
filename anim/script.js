// script.js

// Original text to display
const originalText = `Cuando yo tenía 6 años,
leí un libro sobre los animales de la selva.
Ese libro explicaba
que las boas se tragan
a sus presas sin masticarlas.

Después de comer,
pasan 6 meses sin moverse
para hacer la digestión.

Pensé mucho sobre la selva y las boas
e hice el primer dibujo de mi vida.
Era este, mi dibujo número 1:

Enseñé mi dibujo a las personas grandes
y les pregunté si les asustaba,
pero pensaban que era un sombrero
y no entendían mi pregunta.

Las personas grandes nunca comprenden nada
por sí solas,
y es agotador para los niños,
tener que darles explicaciones siempre.`;

// Function to convert text to hexadecimal
function textToHex(text) {
  return text
    .split("")
    .map((char) => char.charCodeAt(0).toString(16))
    .join(" ");
}

// Function to convert text to Braille using Unicode characters
function textToBraille(text) {
  const brailleMap = {
    " ": " ",
    a: "\u2801",
    b: "\u2803",
    c: "\u2809",
    d: "\u2819",
    e: "\u2811",
    f: "\u280B",
    g: "\u281B",
    h: "\u2813",
    i: "\u280A",
    j: "\u281A",
    k: "\u2805",
    l: "\u2807",
    m: "\u280D",
    n: "\u281D",
    o: "\u2815",
    p: "\u280F",
    q: "\u281F",
    r: "\u2817",
    s: "\u280E",
    t: "\u281E",
    u: "\u2825",
    v: "\u2827",
    w: "\u283A",
    x: "\u282D",
    y: "\u283D",
    z: "\u2835",
    á: "\u2837",
    é: "\u282F",
    í: "\u280A",
    ó: "\u2815",
    ú: "\u2825",
    ñ: "\u283B",
    ü: "\u2833",
    ç: "\u2837",
    A: "\u2828\u2801",
    B: "\u2828\u2803",
    C: "\u2828\u2809",
    D: "\u2828\u2819",
    E: "\u2828\u2811",
    F: "\u2828\u280B",
    G: "\u2828\u281B",
    H: "\u2828\u2813",
    I: "\u2828\u280A",
    J: "\u2828\u281A",
    K: "\u2828\u2805",
    L: "\u2828\u2807",
    M: "\u2828\u280D",
    N: "\u2828\u281D",
    O: "\u2828\u2815",
    P: "\u2828\u280F",
    Q: "\u2828\u281F",
    R: "\u2828\u2817",
    S: "\u2828\u280E",
    T: "\u2828\u281E",
    U: "\u2828\u2825",
    V: "\u2828\u2827",
    W: "\u2828\u283A",
    X: "\u2828\u282D",
    Y: "\u2828\u283D",
    Z: "\u2828\u2835",
    Á: "\u2828\u2837",
    É: "\u2828\u282F",
    Í: "\u2828\u280A",
    Ó: "\u2828\u2815",
    Ú: "\u2828\u2825",
    Ñ: "\u2828\u283B",
    Ü: "\u2828\u2833",
    Ç: "\u2828\u2837",
    ".": "\u2804",
    ",": "\u2802",
    ";": "\u2806",
    ":": "\u2812",
    "-": "\u2824",
    "'": "\u2806",
    "`": "\u2830",
    "“": "\u2826",
    "”": "\u2826",
    "(": "\u2863",
    ")": "\u281C",
    "!": "\u2816",
    "¡": "\u2816",
    "?": "\u2822",
    "¿": "\u2822",

    1: "\u283C\u2801",
    2: "\u283C\u2803",
    3: "\u283C\u2809",
    4: "\u283C\u2819",
    5: "\u283C\u2811",
    6: "\u283C\u280B",
    7: "\u283C\u281B",
    8: "\u283C\u2813",
    9: "\u283C\u280A",
    0: "\u283C\u281A",
  };
  return text
    .split("")
    .map((char) => brailleMap[char] || char)
    .join("");
}

// Insert text into the respective sections
document.getElementById("original-text").innerHTML = `<p>${originalText}</p>`;
//document.getElementById("hex-text").innerHTML = `<p style="font-size:1rem;">${textToHex(originalText)}</p>`;
document.getElementById("braille-text").innerHTML = `<p>${textToBraille(
  originalText
)}</p>`;

// Function to add animation classes after specific delays
document
  .getElementById("start-animation")
  .addEventListener("click", function () {
    const originalSection = document.getElementById("original-text");
    const hexSection = document.getElementById("hex-text");
    const brailleSection = document.getElementById("braille-text");

    const animationContainer = document.getElementById("anim-container");
    const originalContent = document.getElementById("original-content");

    originalContent.classList.add("springFadeOut");

    setTimeout(() => {
        originalContent.classList.add("hidden");
        animationContainer.classList.remove("hidden");
    }, 800);

    // Original text appears immediately with movement
    setTimeout(() => {
      originalContent.remove();
      originalSection.classList.add("fade-in");
    }, 1200);

    // Hex text appears after 2 seconds
    /*setTimeout(() => {
    hexSection.classList.add("fade-in-delayed");
  }, 1000);*/

    // Braille text appears after 4 seconds with movement
    setTimeout(() => {
      brailleSection.classList.add("fade-in-more-delayed");
    }, 200);
  });
