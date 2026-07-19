/*
 * 담당자 코멘트 저장 버튼.
 *
 * 이 사이트는 백엔드 서버가 없는 정적 GitHub Pages라, "저장"이 실제로
 * 영구 반영되려면 브라우저에서 곧바로 GitHub API를 호출해 그 리포트
 * HTML 파일을 커밋하는 수밖에 없다. 그러려면 이 저장소에 쓰기 권한이
 * 있는 사용자의 GitHub 토큰이 필요하다 (fine-grained PAT, 이 저장소에만
 * Contents: Read and write 권한). 그 토큰은 절대 서버로 전송되지 않고
 * 이 브라우저의 localStorage에만 저장되며, api.github.com 호출에만
 * 쓰인다.
 */
(function () {
  const REPO = "byungwoo135/nosa-trend-weekly";
  const API = "https://api.github.com";
  const TOKEN_KEY = "nosa_gh_pat";

  function b64EncodeUtf8(str) {
    return btoa(unescape(encodeURIComponent(str)));
  }
  function b64DecodeUtf8(b64) {
    return decodeURIComponent(escape(atob(b64.replace(/\n/g, ""))));
  }
  function escapeHtml(str) {
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  async function saveComment() {
    const path = window.__NOSA_REPORT_PATH;
    const contentEl = document.querySelector(".opinion-content");
    const btn = document.querySelector(".opinion-save-btn");
    const statusEl = document.querySelector(".opinion-save-status");
    if (!path || !contentEl || !btn || !statusEl) return;

    let token = localStorage.getItem(TOKEN_KEY);
    if (!token) {
      token = window.prompt(
        "GitHub 토큰이 필요합니다 (이 저장소 Contents 쓰기 권한이 있는 fine-grained PAT).\n" +
          "한 번만 입력하면 이 브라우저에 저장되어 다음부터는 묻지 않습니다."
      );
      if (!token) return;
      token = token.trim();
      localStorage.setItem(TOKEN_KEY, token);
    }

    const commentText = contentEl.innerText.replace(/\n{3,}/g, "\n\n").trim();
    const originalLabel = btn.textContent;
    btn.disabled = true;
    btn.textContent = "⏳";
    statusEl.textContent = "";

    try {
      const getRes = await fetch(`${API}/repos/${REPO}/contents/${path}`, {
        headers: { Authorization: `Bearer ${token}`, Accept: "application/vnd.github+json" },
      });
      if (!getRes.ok) throw new Error(`파일 조회 실패 (${getRes.status})`);
      const fileData = await getRes.json();
      const currentSource = b64DecodeUtf8(fileData.content);

      const marker = /(<div class="opinion-content"[^>]*>)([\s\S]*?)(<\/div>)/;
      if (!marker.test(currentSource)) throw new Error("코멘트 영역을 찾지 못했습니다");
      const newSource = currentSource.replace(marker, (_, open, _old, close) => {
        return open + escapeHtml(commentText) + close;
      });

      const putRes = await fetch(`${API}/repos/${REPO}/contents/${path}`, {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${token}`,
          Accept: "application/vnd.github+json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: `담당자 코멘트 업데이트 (${path})`,
          content: b64EncodeUtf8(newSource),
          sha: fileData.sha,
          branch: "main",
        }),
      });
      if (!putRes.ok) {
        const err = await putRes.json().catch(() => ({}));
        if (putRes.status === 401 || putRes.status === 403) {
          localStorage.removeItem(TOKEN_KEY);
        }
        throw new Error(err.message || `저장 실패 (${putRes.status})`);
      }

      statusEl.textContent = "✓ 저장됨";
      statusEl.style.color = "#0e7c66";
    } catch (err) {
      statusEl.textContent = "✗ " + err.message;
      statusEl.style.color = "#c0392b";
    } finally {
      btn.disabled = false;
      btn.textContent = originalLabel;
      setTimeout(() => {
        statusEl.textContent = "";
      }, 5000);
    }
  }

  window.__nosaSaveComment = saveComment;
})();
