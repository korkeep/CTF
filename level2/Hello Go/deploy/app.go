package main

import (
	"html/template"
	"net/http"
	"bytes"
	"fmt"
	"strings"
	"github.com/labstack/echo/v4"
)


func greetHandler(c echo.Context) error {
	name := c.QueryParam("name")

	if name == "" {
		name = "go"
	}

	if strings.Contains(strings.ToLower(name),"flag"){
		return c.String(http.StatusBadRequest, "flag is not allowed.")
	}

	t, err := template.New("page").Parse(
		fmt.Sprintf(`
			<html>
			<body>
				<h1>Hello, %s!</h1>
			</body>
			</html>`, name))
	if err != nil {
		return c.String(http.StatusInternalServerError, "Template parse error: "+err.Error())
	}

	buf := new(bytes.Buffer)
	err = t.Execute(buf, c) 
	if err != nil {
		return c.String(http.StatusInternalServerError, "Template execution error: "+err.Error())
	}

	return c.HTMLBlob(http.StatusOK, buf.Bytes())
}

func main() {
	e := echo.New()
	e.GET("/", greetHandler)
	e.Start(":8000")
}
