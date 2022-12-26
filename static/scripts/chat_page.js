class Chatbox {
  constructor() {
    this.args = {
      chatBox: document.querySelector(".chatbox__support"),
      sendButton: document.querySelector(".send__button"),
    };
    this.state = false;
    this.messages = [];
  }

  display() {
    const { sendButton, chatBox } = this.args;

    this.getChatHistory(chatBox);

    sendButton.addEventListener("click", (e) => {
      if (!e.detail || e.detail == 1) {
        return this.onSendButton(chatBox);
      } else {
        return false;
      }
    });

    const node = chatBox.querySelector("input");
    node.addEventListener("keyup", (e) => {
      e.preventDefault();

      if (
        e.key === "Enter" &&
        node.value != "" &&
        !e.shiftKey &&
        this.state == false
      ) {
        this.state = true;
        this.onSendButton(chatBox);
      }
    });
  }

  onSendButton(chatbox) {
    var textField = chatbox.querySelector("input");
    let text1 = textField.value;
    if (text1 === "") {
      return;
    }

    let msg1 = { type: "message", text: text1 };
    this.messages.push(msg1);

    fetch($SCRIPT_ROOT + "/predict", {
      method: "POST",
      body: JSON.stringify({ message: text1 }),
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((r) => r.json())
      .then((r) => {
        let msg2 = { type: "response", text: r.answer };
        this.messages.push(msg2);
        this.updateChatText(chatbox);

        textField.value = "";
        this.state = false;
      })
      .catch((error) => {
        console.error("Error:", error);
        this.updateChatText(chatbox);
        textField.value = "";
        this.state = false;
      });
  }

  updateChatText(chatBox) {
    var html = "";
    this.messages.slice().forEach(function (item, index) {
      if (item.type === "response") {
        html +=
          '<div class="messages__item messages__item--visitor">' +
          item.text +
          "</div>";
      } else {
        html +=
          '<div class="messages__item messages__item--operator">' +
          item.text +
          "</div>";
      }
    });

    const chatmessage = chatBox.querySelector(".chatbox__messages");
    chatmessage.innerHTML = html;

    var xH = chatmessage.scrollHeight;
    chatmessage.scrollTo(0, xH);
  }

  getChatHistory(chatbox) {
    fetch($SCRIPT_ROOT + "/history", {
      method: "GET",
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((r) => r.json())
      .then((r) => {
        var html = "";
        r.slice().forEach(function (item) {
          if (item.type === "response") {
            html +=
              '<div class="messages__item messages__item--visitor">' +
              item.text +
              "</div>";
          } else {
            html +=
              '<div class="messages__item messages__item--operator">' +
              item.text +
              "</div>";
          }
        });

        const chatmessage = chatbox.querySelector(".chatbox__messages");
        chatmessage.innerHTML = html;

        var xH = chatmessage.scrollHeight;
        chatmessage.scrollTo(0, xH);

        this.messages.push(...r);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
}

const chatbox = new Chatbox();
chatbox.display();
