function testes() {
    const chessboardContainer = document.querySelector('.text');
    chessboardContainer.innerHTML = 'GAT'; // Clear existing board   
}
console.log('Bitch dont kill my bive');


function handleClick(pos) {
    console.log("Handle that bith");

    console.log(`Square clicked: ${pos}`);

    fetch('/select-square/', {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(), // Include the CSRF token
        },
        body: JSON.stringify({ "pos": pos })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            switch (data.game) {
                case 2:
                    renderBoard(data.board);
                    const squares = document.querySelectorAll('.square');
    
                    // Loop through each square and add an onclick event listener
                    squares.forEach(square => {
                        square.onclick = function() {
                            const pos = square.getAttribute('pos');
                            handleClick(pos);
                        };
                    });
                    break;
                case 1:
                    renderBoard(data.board);
                    displayText("Black wins by checkmate");
                    break;
                case -1:
                    renderBoard(data.board);
                    displayText("White wins by checkmate");
                    break;
                default:
                    renderBoard(data.board);
                    displayText("Draw");
            }
            console.log("Square processed successfully.");
        } else {
            console.log("Error processing square.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}


function listen() {
    document.addEventListener('DOMContentLoaded', function() {
        // Select all elements with the class 'square'
        console.log("running");
        const squares = document.querySelectorAll('.square');
    
        // Loop through each square and add an onclick event listener
        squares.forEach(square => {
            square.onclick = function() {
                const pos = square.getAttribute('pos');
                handleClick(pos);
            };
        });
    });
}


listen();

console.log("KILIAK");

// applySquareListeners();

function renderBoard(board) {
    
    if (board == null) {
        return
    }
    const chessboardContainer = document.querySelector('.chessboard');
    chessboardContainer.innerHTML = ''; // Clear existing board

    board.forEach((row) => {
        row.forEach((col) => {
            const square = document.createElement('div');
            square.className = `square ${col.color}`;  // Set class to color (white or black)
            square.setAttribute('pos', col.pos);  // Set the position as a data attribute

            // If there's a piece, add an image of the piece
            if (col.piece) {
                const pieceImg = document.createElement('img');
                pieceImg.src = `/static/chessapp/images/${col.piece}.png`;
                pieceImg.alt = col.piece;
                pieceImg.classList.add('piece');  // Add class for styling the piece
                square.appendChild(pieceImg);
            }

            chessboardContainer.appendChild(square); // Add the square to the board container
        });
        console.log("render that bith");
        
    });
}


// function applySquareListeners() {
//     console.log("apply that bith");
//     document.querySelectorAll('.square').forEach(square => {
//         square.addEventListener('click', function () {
//             const pos = this.getAttribute('pos');
    
//             console.log(`Square clicked: ${pos}`);
    
//             // Send the selected square to the backend
//             fetch('/select-square/', {
//                 method: 'POST',
//                 headers: { 
//                     'Content-Type': 'application/json',
//                     'X-CSRFToken': getCSRFToken(), // Include the CSRF token
//                 },
//                 body: JSON.stringify({ "pos": pos })
//             })
//             .then(response => response.json())
//             .then(data => {
//                 if (data.success) {
//                     switch (data.game) {
//                         case 2:
//                             renderBoard(data.board);
//                             break;
//                         case 1:
//                             renderBoard(data.board);
//                             displayText("Black wins by checkmate");
//                             break;
//                         case -1:
//                             renderBoard(data.board);
//                             displayText("White wins by checkmate");
//                             break;
//                         default:
//                             renderBoard(data.board);
//                             displayText("Draw");
//                     }
//                     console.log("Square processed successfully.");
//                 } else {
//                     console.log("Error processing square.");
//                 }
//             })
//             .catch(error => {
//                 console.error("Error:", error);
//             });
//         }, {once: true});
//     });
// }


function displayText(text) {
    const itemContainer = document.querySelector('.text');
    itemContainer.innerHTML = text; // add board
}

// Function to get CSRF token
function getCSRFToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue;
}
