// Flash message auto-dismiss
document.querySelectorAll('.flash-close').forEach(btn => {
  btn.addEventListener('click', () => btn.closest('.flash').remove());
});
setTimeout(() => {
  document.querySelectorAll('.flash').forEach(el => {
    el.style.transition = 'opacity .4s';
    el.style.opacity = '0';
    setTimeout(() => el.remove(), 400);
  });
}, 5000);

// Hamburger nav toggle
const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');
if (hamburger && navLinks) {
  hamburger.addEventListener('click', () => navLinks.classList.toggle('open'));
}

// Chatbot logic
const chatWindow = document.getElementById('chatWindow');
if (chatWindow) {
  let step = 0;
  let sessionData = {};

  function appendMsg(text, sender) {
    const wrap = document.createElement('div');
    wrap.className = `chat-msg ${sender}`;
    const avatar = document.createElement('div');
    avatar.className = 'chat-avatar';
    avatar.textContent = sender === 'bot' ? '🤖' : '👤';
    const bubble = document.createElement('div');
    bubble.className = 'chat-bubble';
    // Convert **bold** markdown
    bubble.innerHTML = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');
    wrap.appendChild(avatar);
    wrap.appendChild(bubble);
    chatWindow.appendChild(wrap);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    return wrap;
  }

  function showOptions(options) {
    if (!options || !options.length) return;
    const container = document.createElement('div');
    container.className = 'chat-msg bot';
    const avatar = document.createElement('div');
    avatar.className = 'chat-avatar';
    avatar.textContent = '🤖';
    const opts = document.createElement('div');
    opts.className = 'chat-options';
    options.forEach(opt => {
      const btn = document.createElement('button');
      btn.className = 'chat-option-btn';
      btn.textContent = opt;
      btn.onclick = () => { sendMessage(opt); container.remove(); };
      opts.appendChild(btn);
    });
    container.appendChild(avatar);
    container.appendChild(opts);
    chatWindow.appendChild(container);
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }

  function showTyping() {
    const el = document.createElement('div');
    el.className = 'chat-msg bot';
    el.id = 'typing';
    el.innerHTML = '<div class="chat-avatar">🤖</div><div class="chat-bubble"><div class="typing-indicator"><div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div></div></div>';
    chatWindow.appendChild(el);
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }

  function removeTyping() {
    const t = document.getElementById('typing');
    if (t) t.remove();
  }

  async function sendMessage(text) {
    if (!text.trim()) return;
    const input = document.getElementById('chatInput');
    if (input) input.value = '';
    if (text !== '__init__') appendMsg(text, 'user');
    showTyping();
    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text === '__init__' ? '' : text, step, session_data: sessionData })
      });
      const data = await res.json();
      removeTyping();
      setTimeout(() => {
        appendMsg(data.response, 'bot');
        step = data.next_step;
        sessionData = data.session_data || {};
        if (data.options) showOptions(data.options);
        if (data.done && data.complaint_id) {
          setTimeout(() => {
            appendMsg(`🎉 Complaint #${data.complaint_id} filed! <a href="/track/${data.complaint_id}" style="color:var(--primary)">Track it here</a>`, 'bot');
          }, 600);
        }
      }, 400);
    } catch(e) {
      removeTyping();
      appendMsg('Sorry, something went wrong. Please try again.', 'bot');
    }
  }

  // Init chatbot
  sendMessage('__init__');

  const sendBtn = document.getElementById('chatSend');
  const chatInput = document.getElementById('chatInput');
  if (sendBtn) sendBtn.addEventListener('click', () => { sendMessage(chatInput.value); });
  if (chatInput) chatInput.addEventListener('keypress', e => { if (e.key === 'Enter') sendMessage(chatInput.value); });
}

// Complaint form: preview AI analysis
const descField = document.getElementById('description');
const titleField = document.getElementById('title');
if (descField && titleField) {
  let debounceTimer;
  function analyzePreview() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(async () => {
      const title = titleField.value.trim();
      const desc = descField.value.trim();
      if (!title && !desc) return;
      const preview = document.getElementById('aiPreview');
      if (!preview) return;
      preview.style.display = 'block';
    }, 500);
  }
  descField.addEventListener('input', analyzePreview);
  titleField.addEventListener('input', analyzePreview);
}
