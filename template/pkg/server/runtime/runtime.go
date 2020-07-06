package runtime

import (
	"github.com/emicklei/go-restful"
)

const (
	//ApiRootPath = "/api"
	ApiRootPath = ""
)

// container holds all webservice
var Container = restful.NewContainer()

type ContainerBuilder []func(c *restful.Container) error

const MimeMergePatchJson = "application/merge-patch+json"
const MimeJsonPatchJson = "application/json-patch+json"

func init() {
	restful.RegisterEntityAccessor(MimeMergePatchJson, restful.NewEntityAccessorJSON(restful.MIME_JSON))
	restful.RegisterEntityAccessor(MimeJsonPatchJson, restful.NewEntityAccessorJSON(restful.MIME_JSON))
}

func NewWebService(gv GroupVersion) *restful.WebService {
	webservice := restful.WebService{}
	webservice.Path(ApiRootPath + "/" + gv.String()).
		Consumes(restful.MIME_JSON).
		Produces(restful.MIME_JSON)

	return &webservice
}

func (cb *ContainerBuilder) AddToContainer(c *restful.Container) error {
	for _, f := range *cb {
		if err := f(c); err != nil {
			return err
		}
	}
	return nil
}

func (cb *ContainerBuilder) Register(funcs ...func(*restful.Container) error) {
	for _, f := range funcs {
		*cb = append(*cb, f)
	}
}

func NewContainerBuilder(funcs ...func(*restful.Container) error) ContainerBuilder {
	var cb ContainerBuilder
	cb.Register(funcs...)

	return cb
}

// Must panics on non-nil errors.  Useful to handling programmer level errors.
func Must(err error) {
	if err != nil {
		panic(err)
	}
}
