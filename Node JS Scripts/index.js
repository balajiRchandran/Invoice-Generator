var express = require('express');
var bodyParser = require('body-parser');
var app = express();
const fs = require("fs");
const PDFDocument = require("pdfkit");
var nodemailer = require('nodemailer');

const port = process.env.PORT || 3000;
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

function generateHeader(doc) {
  doc
    .image("logo.jpg", 50, 45, { width: 100 })
    .fillColor("#444444")
    .fontSize(10)
    .text("Pied Piper Inc.", 200, 50, { align: "right" })
    .text("5230,Newell Road", 200, 65, { align: "right" })
    .text("Palo Alto,California", 200, 80, { align: "right" })
    .moveDown();
}

function generateCustomerInformation(doc, invoice) {
  doc
    .fillColor("#444444")
    .fontSize(20)
    .text("Invoice", 50, 160);

  generateHr(doc, 185);

  const customerInformationTop = 200;

  doc
    .fontSize(10)
    .text("Invoice Number:", 50, customerInformationTop)
    .font("Helvetica-Bold")
    .text(invoice.invoice_nr, 150, customerInformationTop)
    .font("Helvetica")
    .text("Invoice Date:", 50, customerInformationTop + 15)
    .text(formatDate(new Date()), 150, customerInformationTop + 15)
    .text("Balance Due:", 50, customerInformationTop + 30)
    .text(
      formatCurrency(invoice.due),
      150,
      customerInformationTop + 30
    )

    .font("Helvetica-Bold")
    .text(invoice.shipping.name, 300, customerInformationTop)
    .font("Helvetica")
    .text(invoice.shipping.address, 300, customerInformationTop + 15)
    .text(
      invoice.shipping.city +
        "-" +
        invoice.shipping.pin,
      300,
      customerInformationTop + 30
    )
    .moveDown();

  generateHr(doc, 252);
}

function generateInvoiceTable(doc, invoice) {
  let i;
  const invoiceTableTop = 330;

  doc.font("Helvetica-Bold");
  generateTableRow(
    doc,
    invoiceTableTop,
    "Item",
    "Unit Cost",
    "Quantity",
    "Tax%",
    "Tax Amount",
    "Line Total"
  );
  generateHr(doc, invoiceTableTop + 20);
  doc.font("Helvetica");

  for (i = 0; i < invoice.items.length; i++) {
    const item = invoice.items[i];
    const position = invoiceTableTop + (i + 1) * 30;
    generateTableRow(
      doc,
      position,
      item.Item,
      formatCurrency(item.Price),
      item.Quan,
      item.Tax,
      formatCurrency(item.taxamnt),
      formatCurrency(item.line)
    );

    generateHr(doc, position + 20);
  }

  const subtotalPosition = invoiceTableTop + (i + 1) * 30;
  doc.font("Helvetica-Bold");
  generateTableRow(
    doc,
    subtotalPosition,
    "",
    "",
    "",
    "Balance Due",
    "",
    formatCurrency(invoice.due)
  );
  doc.font("Helvetica");
}

function generateFooter(doc) {
  doc
    .fontSize(10)
    .text(
      "Payment is due within 10 days. Thank you for your business.",
      50,
      780,
      { align: "center", width: 500 }
    );
}

function generateTableRow(
  doc,
  y,
  item,
  unitCost,
  quantity,
  tax,
  taxamnt,
  lineTotal
) {
  doc
    .fontSize(10)
    .text(item, 50, y)
    .text(unitCost, 160, y)
    .text(quantity, 230, y, { width: 70, align: "right" })
    .text(tax, 300, y, { width: 70, align: "right" })
    .text(taxamnt, 390, y, { width: 70, align: "right" })
    .text(lineTotal, 0, y, { align: "right" });
}

function generateHr(doc, y) {
  doc
    .strokeColor("#aaaaaa")
    .lineWidth(1)
    .moveTo(50, y)
    .lineTo(550, y)
    .stroke();
}

function formatCurrency(cents) {
  return "Rs " +cents;
}

function formatDate(date) {
  const day = date.getDate();
  const month = date.getMonth() + 1;
  const year = date.getFullYear();

  return year + "/" + month + "/" + day;
}
app.get("/postdata", (req, res) => {
    var invoice=JSON.parse(req.body.data);
    //console.log(invoice);
    let doc = new PDFDocument({ size: "A4", margin: 50 });
    generateHeader(doc);
    generateCustomerInformation(doc, invoice);
    generateInvoiceTable(doc, invoice);
    generateFooter(doc);
    doc.pipe(fs.createWriteStream(__dirname+"/invoice.pdf")).on('finish',function(){
      var mail = nodemailer.createTransport({
        service: 'gmail',
        auth: {
          user: 'your-mail',
          pass: 'your-pass'
        }
      });
      res.download(__dirname+"/invoice.pdf");
        var mailOptions = {
          from: 'your-mail',
          to: invoice.cmail,
          subject: 'Invoice-'+invoice.invoice_nr,
          text: 'Thanks for your business with us! Find the invoice attached with this mail and the payment is due within 10 days \n\nThanks and Regards,\nPied Piper Inc.',
          attachments: [{path: __dirname+"/invoice.pdf"}]
        };
        mail.sendMail(mailOptions, function(error, info){
          if (error) {
            console.log(error);
          } else {
            console.log('Email sent: ' + info.response);
          }
    });
    
});
    doc.end();
});
app.listen(port);