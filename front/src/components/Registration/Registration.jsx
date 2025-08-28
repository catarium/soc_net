import "./Registration.css";
import React, { useState } from "react";

export default function Registration() {
    const [form, setForm] = useState(
        {
            name: "",
            password: "",
        },
    );
    const handleChange = (e) => {
        const { name, value } = e.target;
        setForm((prevForm) => ({
            ...prevForm,
            [name]: value,
        }));
    };
    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await fetch("/api/auth/registration", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(form),
            credentials: "include",
        });

        if (!response.ok) {
            alert("error");
        }
        // navigate("/");
    };
    return (
        <>
            <div className="Registration">
                <div className="FormBlock">
                    <div className="FormEl">
                        <div className="FormLabel">
                            Name
                        </div>
                        <div className="FormInputBox">
                            <input
                                type="text"
                                id="name"
                                name="name"
                                className="TextInput"
                                onChange={handleChange}
                            >
                            </input>
                        </div>
                    </div>
                    <div className="FormEl">
                        <div className="FormLabel">
                            Password
                        </div>
                        <div className="FormInputBox">
                            <input
                                type="password"
                                id="password"
                                name="password"
                                className="TextInput"
                                onChange={handleChange}
                            >
                            </input>
                        </div>
                    </div>
                    <div className="FormEl">
                        <button onClick={handleSubmit}>Sign up</button>
                    </div>
                </div>
            </div>
        </>
    );
}
