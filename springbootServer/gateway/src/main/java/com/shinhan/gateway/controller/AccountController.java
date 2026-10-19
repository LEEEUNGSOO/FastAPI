package com.shinhan.gateway.controller;

import com.shinhan.gateway.dto.BalanceResponse;
import com.shinhan.gateway.dto.CategorySummaryResponse;
import com.shinhan.gateway.dto.TransactionResponse;
import java.util.List;
import java.util.Optional;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestClient;

@RestController
@RequestMapping("/api/accounts")                         // 이 클래스 주소는 전부 /api/accounts 로 시작
public class AccountController {

    private final RestClient fastApiClient;

    public AccountController(RestClient fastApiClient) {    // 생성자 주입 (RestClientConfig 의 Bean)
        this.fastApiClient = fastApiClient;
    }

    // 1. 잔액  Postman: GET /api/accounts/A001/balance  →  FastAPI: GET /accounts/A001/balance
    @GetMapping("/{accountId}/balance")
    public BalanceResponse balance(@PathVariable("accountId") String accountId) {   // 이름을 꼭 적기
        return fastApiClient.get()                                // ① GET
                .uri("/accounts/{id}/balance", accountId)         // ② {id} ← A001
                .retrieve()                                       // ③ 보내고 받기 (실패하면 여기서 예외)
                .body(BalanceResponse.class);                     // ④ JSON → record
    }

    // 2. 거래내역  ?start=&end=&category= 는 값이 있을 때만 FastAPI에 전달
    //Optional : 옵셔널 — 값이 있을 수도, 없을 수도 있음을 표현하는 Java 클래스
    //ofNullable() : 오브 널러블 — null 여부에 따라 Optional 객체를 생성하는 메서드
    @GetMapping("/{accountId}/transactions")
    public List<TransactionResponse> transactions(
            @PathVariable("accountId") String accountId,
            @RequestParam(name = "start", required = false) String start,
            @RequestParam(name = "end", required = false) String end,
            @RequestParam(name = "category", required = false) String category) {
        return fastApiClient.get()
                .uri(uriBuilder -> uriBuilder
                        .path("/accounts/{id}/transactions")
                        .queryParamIfPresent("start", Optional.ofNullable(start))         // null이면 안 붙임
                        .queryParamIfPresent("end", Optional.ofNullable(end))
                        .queryParamIfPresent("category", Optional.ofNullable(category))   // 한글도 자동 인코딩
                        .build(accountId))                                                // {id} ← A001
                .retrieve()
                .body(new ParameterizedTypeReference<List<TransactionResponse>>() {});   // 리스트로 받기
    }

    // 3. 카테고리 요약
    @GetMapping("/{accountId}/summary")
    public List<CategorySummaryResponse> summary(@PathVariable("accountId") String accountId) {
        return fastApiClient.get()
                .uri("/accounts/{id}/summary", accountId)
                .retrieve()//HTTP 응답을 가져와 처리하는 단계 설정
                //.body()	실제 요청을 실행하고 JSON을 DTO로 변환
                .body(new ParameterizedTypeReference<List<CategorySummaryResponse>>() {});
    }
}

/* ===== 전체 이해 =====
 * - Postman이 부르는 주소 3개를 받아서, 같은 모양의 FastAPI 주소로 그대로 넘깁니다.
 * - 실행 순서 (잔액)
 *     ① Postman → :8080/api/accounts/A001/balance
 *     ② balance("A001") 실행
 *     ③ RestClient → :8000/accounts/A001/balance
 *     ④ FastAPI JSON → BalanceResponse record
 *     ⑤ return → Spring이 다시 JSON으로 → Postman
 * - @PathVariable("accountId") 처럼 괄호에 이름을 적는 이유:
 *   Spring Boot 3.2부터 이름을 안 적으면 IntelliJ 빌드에서
 *   "Name for argument of type [java.lang.String] not specified" 에러가 날 수 있음
 * - 리스트는 List<...>.class 를 쓸 수 없어서(제네릭) ParameterizedTypeReference 로 타입을 넘김
 * - 쿼리는 "?category=" + category 처럼 문자열로 붙이지 않음 (한글·null 문제)
 * - Service 가 없는 이유: 오늘은 전달만. 업무 규칙이 생기는 6·7일차에 Service 추가
 */