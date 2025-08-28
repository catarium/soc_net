export default async function uploadMedia(media) {
    const data = new FormData();
    for (const m of media) {
        data.append("files", m, m.name);
    }
    const resp = await fetch("/api/userapi/media/", {
        method: "POST",
        body: data,
    });
    return resp;
}
