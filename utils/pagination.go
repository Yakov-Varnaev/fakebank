package pagination

import (
	"net/http"
	"strconv"

	httpErrors "github.com/Yakov-Varnaev/fakebank/errors"
	"github.com/doug-martin/goqu/v9"
	"github.com/gin-gonic/gin"
)

type Params struct {
	Offset uint
	Limit  uint
}

func FromContext(c *gin.Context) (*Params, error) {
	var err error
	p := &Params{}
	offset, err := strconv.Atoi(c.DefaultQuery("offset", "0"))
	if err != nil {
		return p, &httpErrors.HTTPError{
			Code: http.StatusBadRequest, Message: "Invalid offset",
		}
	}
	p.Offset = uint(offset)
	limit, err := strconv.Atoi(c.DefaultQuery("limit", "10"))
	if err != nil {
		return p, &httpErrors.HTTPError{
			Code: http.StatusBadRequest, Message: "Invalid limit",
		}
	}
	p.Limit = uint(limit)
	return p, nil
}

func (p *Params) Paginate(dataset *goqu.SelectDataset) *goqu.SelectDataset {
	return dataset.Offset(p.Offset).Limit(p.Limit)
}

type Page[Object any] struct {
	Total int64    `json:"total"`
	Data  []Object `json:"data"`
}
