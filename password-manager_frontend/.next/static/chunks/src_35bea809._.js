(globalThis.TURBOPACK || (globalThis.TURBOPACK = [])).push([typeof document === "object" ? document.currentScript : undefined,
"[project]/src/api/envVars.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "getEnvVar",
    ()=>getEnvVar,
    "getIntEnvVar",
    ()=>getIntEnvVar
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2d$runtime$2d$env$2f$build$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next-runtime-env/build/index.js [app-client] (ecmascript)");
;
const getEnvVar = (key, fallbackValue)=>{
    return (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2d$runtime$2d$env$2f$build$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["env"])('NEXT_PUBLIC_' + key) || fallbackValue;
};
const getIntEnvVar = (key, fallbackValue)=>{
    return parseInt(getEnvVar(key, fallbackValue));
};
;
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/src/api/axiosClient.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>__TURBOPACK__default__export__
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$axios$2f$lib$2f$axios$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/axios/lib/axios.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$api$2f$envVars$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/api/envVars.ts [app-client] (ecmascript)");
;
;
const axiosClient = __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$axios$2f$lib$2f$axios$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].create({
    baseURL: (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$api$2f$envVars$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["getEnvVar"])('API_BASE_URL', ("TURBOPACK compile-time value", "http://localhost:8000"))
});
const __TURBOPACK__default__export__ = axiosClient;
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/src/api/apis.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "createMainUser",
    ()=>createMainUser,
    "createSubAccount",
    ()=>createSubAccount,
    "deleteMainUser",
    ()=>deleteMainUser,
    "deleteSubAccount",
    ()=>deleteSubAccount,
    "getMainUserByKeycloakId",
    ()=>getMainUserByKeycloakId,
    "getSubAccountsByUserId",
    ()=>getSubAccountsByUserId,
    "updateMainUser",
    ()=>updateMainUser,
    "updateSubAccount",
    ()=>updateSubAccount
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$api$2f$axiosClient$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/api/axiosClient.ts [app-client] (ecmascript)");
;
__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$api$2f$axiosClient$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].defaults.headers.common['Content-Type'] = 'application/json';
const createMainUser = async (user)=>{
    try {
        await __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$api$2f$axiosClient$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].post('/mainUser', user);
    } catch (error) {
        console.error('Error creating main user:', error);
        throw error;
    }
};
const getMainUserByKeycloakId = async (keycloak_user_id)=>{
    try {
        const response = await __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$api$2f$axiosClient$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].get("/api/V1/localuser/".concat(keycloak_user_id));
        return response.data.user;
    } catch (error) {
        console.error('Error fetching main user:', error);
        return null;
    }
};
const updateMainUser = async (user)=>{
    try {
        await __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$api$2f$axiosClient$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].put("/api/V1/localuser/".concat(user.Id), user);
    } catch (error) {
        console.error('Error updating main user:', error);
        throw error;
    }
};
const deleteMainUser = async (id)=>{
    try {
        await __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$api$2f$axiosClient$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].delete("/api/V1/localuser/".concat(id));
    } catch (error) {
        console.error('Error deleting main user:', error);
        throw error;
    }
};
const createSubAccount = async (UserId, SubAccount, Salt, MasterPassword)=>{
    try {
        await __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$api$2f$axiosClient$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].post("/api/V1/subaccount/".concat(UserId, "?salt=").concat(Salt, "&master_password=").concat(MasterPassword), {
            user_id: UserId,
            title: SubAccount.title,
            username: SubAccount.username,
            password: SubAccount.password,
            url: SubAccount.url
        });
    } catch (error) {
        console.error('Error creating sub account:', error);
        throw error;
    }
};
const getSubAccountsByUserId = async (userId)=>{
    try {
        const response = await __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$api$2f$axiosClient$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].get("/api/V1/subaccount/".concat(userId), {
            params: {
                userId
            }
        });
        console.log(response.data);
        return response.data.subaccounts;
    } catch (error) {
        console.error("Error fetching sub accounts:", error);
        return [];
    }
};
const updateSubAccount = async (subaccount, subaccount_id, salt)=>{
    try {
        var _subaccount_title, _subaccount_username, _subaccount_password, _subaccount_url;
        await __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$api$2f$axiosClient$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].put("/api/V1/subaccount/".concat(subaccount_id), {
            title: (_subaccount_title = subaccount.title) !== null && _subaccount_title !== void 0 ? _subaccount_title : "",
            username: (_subaccount_username = subaccount.username) !== null && _subaccount_username !== void 0 ? _subaccount_username : "",
            password: (_subaccount_password = subaccount.password) !== null && _subaccount_password !== void 0 ? _subaccount_password : "",
            url: (_subaccount_url = subaccount.url) !== null && _subaccount_url !== void 0 ? _subaccount_url : ""
        }, {
            params: {
                salt: salt
            }
        });
    } catch (error) {
        console.error("Error updating sub account:", error);
        throw error;
    }
};
const deleteSubAccount = async (subaccount_id)=>{
    console.log("Deleting sub account:", {
        subaccount_id
    });
    try {
        await __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$api$2f$axiosClient$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].delete("/api/V1/subaccount/".concat(subaccount_id));
    } catch (error) {
        console.error("Error deleting sub account:", error);
        throw error;
    }
};
;
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/src/app/edit-subaccount/page.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>EditSubAccountPage
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$api$2f$apis$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/api/apis.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/navigation.js [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
"use client";
;
;
;
function EditSubAccountPage() {
    _s();
    const [subAcc, setSubAcc] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    const [salt, setSalt] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    const router = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useRouter"])();
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "EditSubAccountPage.useEffect": ()=>{
            const storedDatas = sessionStorage.getItem("subAccountData");
            const storedUserSalt = sessionStorage.getItem("userSalt");
            if (storedDatas) setSubAcc(JSON.parse(storedDatas));
            if (storedUserSalt) setSalt(storedUserSalt);
        }
    }["EditSubAccountPage.useEffect"], []);
    const handleChange = (e)=>{
        if (!subAcc) return;
        setSubAcc({
            ...subAcc,
            [e.target.name]: e.target.value
        });
    };
    const handleSave = async ()=>{
        if (!subAcc || !salt) return;
        await (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$api$2f$apis$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["updateSubAccount"])(subAcc, subAcc.id, salt);
        alert("Modifiche salvate!");
        router.push("/");
    };
    if (!subAcc) return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        children: "Caricamento dati..."
    }, void 0, false, {
        fileName: "[project]/src/app/edit-subaccount/page.tsx",
        lineNumber: 32,
        columnNumber: 23
    }, this);
    var _subAcc_password;
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "p-6 max-w-lg mx-auto",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h1", {
                className: "text-xl font-bold mb-6",
                children: "Modifica Subaccount"
            }, void 0, false, {
                fileName: "[project]/src/app/edit-subaccount/page.tsx",
                lineNumber: 36,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("form", {
                className: "flex flex-col gap-4",
                onSubmit: (e)=>{
                    e.preventDefault();
                    handleSave();
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                        children: [
                            "Titolo:",
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                type: "text",
                                name: "title",
                                value: subAcc.title,
                                onChange: handleChange,
                                className: "border rounded px-2 py-1 w-full"
                            }, void 0, false, {
                                fileName: "[project]/src/app/edit-subaccount/page.tsx",
                                lineNumber: 40,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/app/edit-subaccount/page.tsx",
                        lineNumber: 38,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                        children: [
                            "Username:",
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                type: "text",
                                name: "username",
                                value: subAcc.username,
                                onChange: handleChange,
                                className: "border rounded px-2 py-1 w-full"
                            }, void 0, false, {
                                fileName: "[project]/src/app/edit-subaccount/page.tsx",
                                lineNumber: 50,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/app/edit-subaccount/page.tsx",
                        lineNumber: 48,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                        children: [
                            "URL:",
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                type: "text",
                                name: "url",
                                value: subAcc.url,
                                onChange: handleChange,
                                className: "border rounded px-2 py-1 w-full"
                            }, void 0, false, {
                                fileName: "[project]/src/app/edit-subaccount/page.tsx",
                                lineNumber: 60,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/app/edit-subaccount/page.tsx",
                        lineNumber: 58,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                        children: [
                            "Password:",
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                type: "text",
                                name: "password",
                                value: (_subAcc_password = subAcc.password) !== null && _subAcc_password !== void 0 ? _subAcc_password : "",
                                onChange: handleChange,
                                className: "border rounded px-2 py-1 w-full"
                            }, void 0, false, {
                                fileName: "[project]/src/app/edit-subaccount/page.tsx",
                                lineNumber: 70,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/app/edit-subaccount/page.tsx",
                        lineNumber: 68,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        type: "submit",
                        className: "px-4 py-2 bg-green-600 text-white rounded-lg shadow hover:bg-green-700",
                        children: "Salva modifiche"
                    }, void 0, false, {
                        fileName: "[project]/src/app/edit-subaccount/page.tsx",
                        lineNumber: 78,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/edit-subaccount/page.tsx",
                lineNumber: 37,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/src/app/edit-subaccount/page.tsx",
        lineNumber: 35,
        columnNumber: 5
    }, this);
}
_s(EditSubAccountPage, "IJ+8aHtwS+R3w93zs/R9HiGkfwc=", false, function() {
    return [
        __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useRouter"]
    ];
});
_c = EditSubAccountPage;
var _c;
__turbopack_context__.k.register(_c, "EditSubAccountPage");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
]);

//# sourceMappingURL=src_35bea809._.js.map