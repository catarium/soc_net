import { useState } from "react";
import "./PostForm.css";
import uploadMedia from "../../utils/uploadMedia.js";

export default function PostForm() {
    const [form, setForm] = useState(
        {
            name: "",
            text: "",
            media: [],
        },
    );
    const handleChange = (e) => {
        const { name, value } = e.target;
        console.log(name);
        console.log(value);
        setForm((prevForm) => ({
            ...prevForm,
            [name]: value,
        }));
    };
    const handleMediaChange = (e) => {
        const files = e.target.files;
        console.log(files);
        setForm((prevForm) => ({
            ...prevForm,
            ["media"]: [...files],
        }));
    };
    const handleSubmit = async (e) => {
        const body = { ...form };
        if (form.media.length != 0) {
            const fileNamesResp = await uploadMedia(form.media);
            if (!fileNamesResp.ok) {
                alert(await fileNamesResp.text());
                return;
            }
            body.media = (await fileNamesResp.json()).res.map((
                item,
            ) => (item.filename));
        }
        e.preventDefault();
        const response = await fetch("/api/userapi/post/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
            credentials: "include",
        });

        if (!response.ok) {
            alert("error");
        }
    };
    return (
        <>
            <div className="PostForm">
                <div className="FormBlock">
                    <div className="FormEl">
                        <div className="FormLabel">
                            Title
                        </div>
                        <div className="FormInputBox">
                            <input
                                type="text"
                                id="title"
                                name="name"
                                className="TextInput"
                                onChange={handleChange}
                            >
                            </input>
                        </div>
                    </div>
                    <div className="FormEl">
                        <div className="FormLabel">
                            Text
                        </div>
                        <div className="FormInputBox">
                            <textarea
                                id="text"
                                name="text"
                                className="AreaInput"
                                onChange={handleChange}
                            >
                            </textarea>
                        </div>
                    </div>
                    <div className="FormEl">
                        <div className="FormLabel">
                            Images
                        </div>
                        <div className="FormInputBox">
                            <input
                                type="file"
                                id="images"
                                name="media[]"
                                className="ImageInput"
                                onChange={handleMediaChange}
                                multiple="multiple"
                            >
                            </input>
                        </div>
                    </div>
                    <div className="FormEl">
                        <button onClick={handleSubmit}>Post</button>
                    </div>
                </div>
            </div>
        </>
    );
}
